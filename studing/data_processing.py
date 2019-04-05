import pandas as pd

excel = pd.read_excel("/Users/hushichang/Downloads/食品安全监管数据/食品抽样结果.xls")


# print(excel)
# print(excel.head(10))
# print(excel.index)
# print(excel.values)
# print(excel.columns)
# print(excel.describe())
# print(excel['sample_no抽样单编号'])
# print(excel['Inspection_project检验项目'].value_counts())
# print(excel[-3:])
# print(excel.iloc[-1])
# print(excel[['Specifications规格']].applymap(lambda x: x if x == '散装' else '整装'))

def function(x):
    # if x.strip() == '散装':
    #     return '散装'
    # elif x.strip() == '' or x.strip() == '/':
    #     return '未知'
    # else:
    #     return '整装'
    if pd.isna(x) or x.strip() == '/':
        return '未知'
    elif x.strip() == '散装':
        return '散装'
    else:
        return '整装'


def change_name_to_city(x):
    if pd.isna(x) or x.strip() == '/':
        return ''
    if '市' in x:
        if '省' in x:
            return x[x.index('省') + 1: x.index('市')]
        return x[:x.index('市')]
    elif '县' in x:
        if '省' in x:
            # print("x is {}".format(x))
            return x[x.index('省') + 1: x.index('县')]
        return x[:x.index("县") + 1]
    elif '西安' in x:
        return '西安'
    elif '广州' in x:
        return '广州'
    elif '天津' in x:
        return '天津'
    elif '青岛' in x:
        return '青岛'
    elif '郑州' in x:
        return '郑州'
    else:
        return x


mark = set()


def get_set_of_county(element):
    if (not pd.isna(element)) and element.endswith('县'):
        mark.add(element)


def get_name_of_county():
    data = pd.read_csv("/Users/hushichang/Desktop/结果数据.csv", index_col=0)

    data[['product_unit_address标示生产单位地址']].applymap(get_set_of_county)
    print(mark)


# county_names = {'连江县', '周至县', '成武县', '大厂县', '平邑县', '郫县', '辉县', '郸城县', '高陵县', '平山县', '青川县', '惠安县', '稷山县', '户县', '大荔县',
#                 '温县', '内黄县', '西乡县', '梁山县', '海丰县', '闽侯县', '徐水县', '礼泉县', '封丘县', '原阳县', '米脂县', '饶平县', '泾阳县', '汤阴县', '淳化县',
#                 '临沂县', '青木县', '岐山县', '邹平县', '正定县'}
# print(len(county_names))
# haha = {"户县": "西安", "大荔县": "渭南", "温县": "焦作", "内黄县": "安阳", "西乡县": "汉中", "梁山县": "济宁", "海丰县": "汕尾", "闽侯县": "福州",
#         "徐水县": "保定", "礼泉县": "咸阳", "封丘县": "新乡", "原阳县": "新乡", "米脂县": "榆林", "饶平县": "潮州", "泾阳县": "咸阳", "汤阴县": "安阳",
#         "淳化县": "咸阳", "临沂县": "临沂", "青木县":"", "岐山县":"宝鸡", "邹平县":"滨州", "正定县":"石家庄"}

data = pd.read_csv("/Users/hushichang/Desktop/test.csv")
print(data)
# print(data[["product_unit_address标示生产单位地址"]].loc[0])
cur = 0
length = 7072
for column in data.columns.values:
    mark = dict()
    for ind in range(length):
        element = data.loc[ind, column]
        if pd.isna(element) or (not element) or (not element.strip()):
            data.loc[ind, column] = column
        else:
            data.loc[ind, column] = element.strip()
data.to_csv("/Users/hushichang/Desktop/no_special_processed.csv", index=0, header=0)

# cur = 1
# for column in data.columns.values:
#     mark = set()
#
# print(data[[data.columns.values[0]]].tolist())
# data[['product_unit_address标示生产单位地址']] = data[['product_unit_address标示生产单位地址']].applymap(lambda x: haha.get(x, x))
# data.to_csv("/Users/hushichang/Desktop/haha.csv")
# excel[['product_unit_address标示生产单位地址']] = excel[['product_unit_address标示生产单位地址']].applymap(change_name_to_city)
# # print(excel[['product_unit_address标示生产单位地址']].applymap(change_name_to_city))
# print(excel[['product_unit_address标示生产单位地址', 'sample_link抽样环节', 'area_name行政区域', 'Sample_large_class样品大类',
#              'Specifications规格', 'inspection_agency检测机构', 'Whether_qualified是否合格']].to_csv("/Users/hushichang/processed_data2.csv"))
# # print(excel['Specifications规格'])
# print(excel.columns.values)


# get_name_of_county()
