from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import re
import csv
from datetime import datetime
from enum import Enum

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, 'data.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class ModelStatus(Enum):
    """Status of model"""
    ENABLED = 1
    DISABLED = 2

    def __repr__(self):
        return u'{name} {value}'.format(name=self.name, value=self.value)


class APICateogryType(Enum):
    """API Cateogry"""
    AUDIO = u"语音"
    FIGURE = u"人像"
    IMAGE = u"图片"
    TEXT = u"文字"
    VIDEO = u"视频"
    OTHERS = u"其他"

    def __repr__(self):
        return u'{name} {value}'.format(name=self.name, value=self.value)


class Tag(db.Model):
    """Tag model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    num_of_datasets = db.Column(db.Integer, nullable=False, default=0)
    num_of_apis = db.Column(db.Integer, nullable=False, default=0)
    baseline = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return u'{id} {name}'.format(id=self.id, name=self.name)


class SourceType(Enum):
    """Source Type"""
    SCREENSHOT = "screenshot"
    TECH_DOC = "tech_doc"
    SOURCE_CODE = "source_code"
    SERVICE_SOURCE = "service_source"

    def __repr__(self):
        return u'{name} {value}'.format(name=self.name, value=self.value)


# 真正要导入的数据，要用到的模型是下面的三个
class ApiLib(db.Model):
    """API Lib model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), unique=True, nullable=False)
    api_platform = db.Column(db.String(80))
    category = db.Column(db.Enum(APICateogryType), nullable=False, default=APICateogryType.AUDIO)
    released_at = db.Column(db.DateTime)
    released_by = db.Column(db.String(80))
    description = db.Column(db.Text)
    url = db.Column(db.String(2048))
    price = db.Column(db.String(512))
    sample_code = db.Column(db.Text)  # HTML probably
    stats_baseline = db.Column(db.Integer, nullable=False, default=0)
    num_of_views = db.Column(db.Integer, nullable=False, default=0)
    num_of_downloads = db.Column(db.Integer, nullable=False, default=0)
    num_of_error_reports = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Enum(ModelStatus), nullable=False, default=ModelStatus.DISABLED)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return u'{id} {name}'.format(id=self.id, name=self.name)


# tag_id 都为空，怎么传数据
class ApiLibTag(db.Model):
    """APILib to Tag relationship"""
    id = db.Column(db.Integer, primary_key=True)
    api_lib_id = db.Column(db.Integer(), db.ForeignKey(ApiLib.id), nullable=False)
    api_lib = db.relationship(ApiLib)
    tag_id = db.Column(db.Integer(), db.ForeignKey(Tag.id), nullable=False)
    tag = db.relationship(Tag)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('tag_id', 'api_lib_id', name='uix_1'),
    )

    def __repr__(self):
        return u'{id} {api_lib} {tag}'.format(id=self.id, tag=self.tag_id, api_lib=self.api_lib_id)


class ApiLibSource(db.Model):
    """API Lib Source model"""
    id = db.Column(db.Integer, primary_key=True)
    api_lib_id = db.Column(db.Integer(), db.ForeignKey(ApiLib.id), nullable=False)
    api_lib = db.relationship(ApiLib)
    source_type = db.Column(db.Enum(SourceType), nullable=False, default=SourceType.SOURCE_CODE)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(2048))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('api_lib_id', 'name', 'source_type', name='uix_1'),
    )

    def __repr__(self):
        return u'{id} {name} {source_type}'.format(
            id=self.id, name=self.name, source_type=self.source_type)


# 数据集的导入需要用的model
class Dataset(db.Model):
    """Dataset model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), unique=True, nullable=False)
    released_at = db.Column(db.DateTime)
    released_by = db.Column(db.String(80))
    description = db.Column(db.Text)
    data_size_in_kb = db.Column(db.Integer)
    url = db.Column(db.String(2048))
    num_of_rows = db.Column(db.Integer)
    stats_baseline = db.Column(db.Integer, nullable=False, default=0)
    num_of_views = db.Column(db.Integer, nullable=False, default=0)
    num_of_downloads = db.Column(db.Integer, nullable=False, default=0)
    num_of_error_reports = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Enum(ModelStatus), nullable=False, default=ModelStatus.DISABLED)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return u'{id} {name}'.format(id=self.id, name=self.name)

class DatasetTag(db.Model):
    """Dataset to Tag relationship"""
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer(), db.ForeignKey(Dataset.id), nullable=False)
    dataset = db.relationship(Dataset)
    tag_id = db.Column(db.Integer(), db.ForeignKey(Tag.id), nullable=False)
    tag = db.relationship(Tag)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('tag_id', 'dataset_id', name='uix_1'),
    )

    def __repr__(self):
        return u'{id} {dataset} {tag}'.format(id=self.id, tag=self.tag_id, dataset=self.dataset_id)

class DatasetSample(db.Model):
    """Dataset Sample model"""
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer(), db.ForeignKey(Dataset.id), nullable=False)
    dataset = db.relationship(Dataset)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(2048))
    size_in_kb = db.Column(db.Integer)
    num_of_rows = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('dataset_id', 'name', name='uix_1'),
    )

    def __repr__(self):
        return u'{id} {name}'.format(
            id=self.id, name=self.name)

class DatasetEssay(db.Model):
    """Dataset Essay model"""
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer(), db.ForeignKey(Dataset.id), nullable=False)
    dataset = db.relationship(Dataset)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(2048))
    download_url = db.Column(db.String(2048))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('dataset_id', 'name', name='uix_1'),
    )

    def __repr__(self):
        return u'{id} {name}'.format(id=self.id, name=self.name)


def preprocess(file):
    # with open(file, 'r', newline='', encoding='GB18030', errors='ignore') as oldfile:
    with open(file, 'r', newline='') as oldfile:
        csvfile = csv.reader(oldfile)
        # 转换朝向
        rows = list(map(list, zip(*list(csvfile))))
        # 存到一个新的文件
        newfile = file[:-4] + '_new' + file[-4:]
        print("newfile is {}".format(newfile))
        with open(newfile, 'w', newline='') as new_file:
            csvWriter = csv.writer(new_file)
            csvWriter.writerows(rows)
        # 读刚存的新文件
        with open(newfile, 'r', newline='') as fffile:
            # """
            # 导入数据集中的description
            # """
            # s = set()
            # reader = csv.DictReader(fffile)
            # for item in reader:
            #     if item['数据名称'] in s:
            #         print(item['数据名称'])
            #         continue
            #     s.add(item['数据名称'])
            #     # print('dataSize is {}'.format(dataSize), item['文件大小'])
            #     print(item['概述'])
            #     db.session.query(Dataset).filter(Dataset.name == item['数据名称']).update({'description': item['概述']})
            #     db.session.commit()

            # # 传入数据到datasettag
            # reader = csv.DictReader(fffile)
            # for row in reader:
            #     if not row['关键词']:
            #         continue
            #     row['关键词'] = row['关键词'].replace('\xa0', '')
            #     tags = [ele.strip() for ele in row['关键词'].strip().split(',')]
            #
            #     dataset = Dataset.query.filter_by(name=row['数据名称']).first()
            #     dataset_id = dataset.id
            #
            #     for tag in tags:
            #         tag = Tag.query.filter_by(name=tag).first()
            #         tag_id = tag.id
            #         db.session.add(DatasetTag(dataset=dataset, dataset_id=dataset_id, tag=tag, tag_id=tag_id))
            #         db.session.commit()
            #         print('hehehehe', dataset, dataset_id)
                        # dt = DatasetTag()





            # """
            # 导入数据集
            # """
            # s = set()
            # reader = csv.DictReader(fffile)
            # for item in reader:
            #     if item['文件大小']:
            #         dataSize = float(re.search(r'\d+(\.\d+)?', item['文件大小']).group()) * (1024 * 1024 if 'Gb' in item['文件大小'] else 1024)
            #     else:
            #         dataSize = 0
            #     if item['数据名称'] in s:
            #         print(item['数据名称'])
            #         continue
            #     s.add(item['数据名称'])
            #     # print('dataSize is {}'.format(dataSize), item['文件大小'])
            #     dataSet = Dataset(name=item['数据名称'], url=item['下载地址'], data_size_in_kb=dataSize)
            #     db.session.add(dataSet)
            #     db.session.commit()


            # reader = csv.DictReader(fffile)
            # for ind, row in enumerate(reader):
            #         """
            #         添加tag属性到数据库"""
            #         # 添加tag标签到Tag表里面, 有的里面是一个空字符串，这种情况下应该掠过去
            #         if not row['关键词']:
            #             continue
            #         row['关键词'] = row['关键词'].replace('\xa0', '')
            #         tags = [ele.strip() for ele in row['关键词'].strip().split(',')]
            #         print("tags is {}".format(tags))
            #         for tag in tags:
            #             print('tag is {}'.format(tag))
            #             # 这个filter之后得再用一个函数取出来， 要不然取不出来的
            #             t = Tag.query.filter_by(name=tag).first()
            #             print("t is {}".format(t))
            #             if not t:
            #                 db.session.add(Tag(name=tag))
            #                 db.session.commit()


            reader = csv.DictReader(fffile)
            flag = False
            for ind, row in enumerate(reader):
                if not flag:
                    print('无用的行 {}'.format([row[ele] for ele in row]))
                    if not any(row[ele] for ele in row):
                        flag = True
                else:
                    # 这一步分是往  ApiLibSource 里面存数据的
                    api_lib = ApiLib.query.filter_by(name=row['平台']+row['子类别']).first()
                    api_lib_id = api_lib.id
                    source_type = None
                    if row['技术文档名'] or row['技术文档下载地址']:
                        name = row['技术文档名']
                        url = row['技术文档下载地址']
                        source_type = SourceType.TECH_DOC
                        db.session.add(ApiLibSource(api_lib=api_lib, api_lib_id=api_lib_id, name=name, url=url,
                                                    source_type=source_type))
                        db.session.commit()
                    if row['源代码网页名'] or row['源代码网页地址']:
                        name = row['源代码网页名']
                        url = row['源代码网页地址']
                        source_type = SourceType.SOURCE_CODE
                        db.session.add(ApiLibSource(api_lib=api_lib, api_lib_id=api_lib_id, name=name, url=url,
                                                    source_type=source_type))
                        db.session.commit()
                    if row['截图']:
                        name = '截图'
                        url = row['截图']
                        source_type = SourceType.SCREENSHOT
                        db.session.add(ApiLibSource(api_lib=api_lib, api_lib_id=api_lib_id, name=name, url=url,
                                                    source_type=source_type))
                        db.session.commit()
                    if not source_type:
                        print(""""hehehehehehe""")

            #
            #         # 插入数据到ApiLib
            #         # 这个地方就要处理数据了
            #         # print(row['类别'])
            #         # print("插入一条数据")
            #         # category = row['类别']
            #         # for categ in APICateogryType:
            #         #     if category == categ.value:
            #         #         category = categ
            #         #         print("category is {}".format(category))
            #         # # # 命名方式由neo告诉
            #         # if '下载地址' not in row:
            #         #     row['下载地址'] = ''
            #         # db.session.add(ApiLib(name=row['平台'] + row['子类别'], api_platform=row['平台'], category=category,
            #         #                 released_by=row['发布人'], description=row['概述'], url=row['下载地址'], price=row['报价']))
            #         # db.session.commit()
db.create_all()
# for ele in Tag.query.all():
#     print(ele)
# for ele in ApiLib.query.all():
#     print(ele)
preprocess('/Users/mac/Documents/百度云.csv')
# preprocess('/Users/mac/Documents/百度云.csv')
# a = ApiLib.query.filter_by(name='hehe').first()
# print(a)
# print(a)
# db.session.add(ApiLibTag(app_lit_id=1, app_lib=a, tag_id=0))