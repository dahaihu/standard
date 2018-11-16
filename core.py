# -*- coding: utf8 -*-
from flask_admin.contrib.sqla.filters import BaseSQLAFilter
from flask import Flask, request, flash, redirect, render_template, jsonify, url_for, current_app
from flask_cors import *
from dashboard.extensions import *
from config import config
from flask_admin import Admin, expose, BaseView, AdminIndexView, helpers
from dashboard.extensions import db
from dashboard.a_models import Project, Worker, TaskRecord, TaskArbitration, TaskReview, TaskError, TaskReview, Notify, \
    WorkerWithdraw, DSAdmin, Task, GoldenAnswerRecord
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import EndpointLinkRowAction
from flask_admin.helpers import get_redirect_target
from flask_admin.actions import action
from flask_admin.babel import gettext, ngettext, lazy_gettext
from dashboard.a_repository import task_repo, project_repo, task_record_repo, task_review_repo, worker_withdraw_repo, \
    worker_repo, company_exchange_repo, ds_admin_repo, task_error_repo
from dashboard.commons import enums
import time
from uploads import uploads_path
import os
import csv
import grpc
from dashboard import notify_pb2, notify_pb2_grpc
from sqlalchemy.sql.expression import func
import datetime

_HOST = 'localhost'
_PORT = '5005'
from dashboard.commons.api_exception import ApiException
from dashboard.commons.backend_exception import BackendException
from dashboard.commons.enums import *
import json
from jinja2 import Markup
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from dashboard.commons.image_annotation import ImageAnnotation
import json
import flask_login as login
from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash
from dashboard.commons.upload import Upload
import requests
from dashboard.a_models import Worker
from dashboard.a_repository import task_record_repo
from jinja2.ext import do
from jinja2 import Environment
from raven.contrib.flask import Sentry

sentry = Sentry()


class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
            # to compare plain text passwords use
            # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return ds_admin_repo.filter_one(login=self.login.data)


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if ds_admin_repo.get_count(self.login.data) > 0:
            raise validators.ValidationError('Duplicate username')


# Initialize flask-login
def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return ds_admin_repo.get_one(user_id)


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProjectModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('.login_view'))
    can_view_details = True
    # column_exclude_list = ['answer_price','audit_price', 'wrong_answer_penalty', 'wrong_audit_penalty',  'close_type','pass_similarity', 'tolerance', 'process', ]
    column_list = ['id', 'name', 'avatar', 'desc', 'status', 'expire_time', 'confidence', 'template_id', 'answer_price',
                   'audit_price', 'answer_number', 'task_process', 'precision', 'created_at', ]
    column_labels = dict(id='id', desc='描述', name='项目名称', avatar='头像', created_at='创建时间', status='状态',
                         expire_time='有效期至', answer_price='答题价', answer_number='答题人数', task_process='进度',
                         precision='审核次数')
    column_searchable_list = ['name', 'id']
    column_filters = ['id', 'name', 'company_id', 'template_id']
    column_auto_select_related = True
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'desc': CKTextAreaField
    }
    column_sortable_list = ('id', 'name', 'avatar', 'desc', 'status', 'template_id', 'answer_price',
                            'audit_price', 'answer_number', 'task_process', 'precision', 'created_at')
    column_default_sort = ('id', True)

    @action('批量审核', '批量审核', '确定审核这些项目吗?')
    def action_batch_active(self, ids):
        return_url = get_redirect_target() or self.get_url('.index_view')
        for id in ids:

            model = self.get_one(id)

            if model is None:
                flash(gettext('project不存在'), 'error')
                return redirect(return_url)

            if model.status == 5:
                flash(gettext('已经审核通过， 无需重复审核.'), 'warning')
                return redirect(return_url)
            request_project_validation(id)
        redirect(return_url)

    @action("统计worker做题数据", "统计worker做题数据", "确定要统计这些项目下的用户做题情况吗？")
    def func(self, ids):
        # 获取所有的workers
        workers = set()
        for i in ids:
            # self.get_one(i) 返回的是一个project
            for ele in self.get_one(i).workers_in_project():
                workers.update(set(ele))
        # 所有项目id，类型转化为整型
        project_ids = [int(i) for i in ids]
        # 一个字典，是worker_id到worker用户的映射
        workerid_to_phone = Worker.worker_id_to_worker_phoneNumber(*workers)
        result = task_record_repo.count_worker_completed_task_and_moderate(workers, project_ids)
        return self.render('workers_statistics.html', workers=result, project_ids=project_ids, mark=workerid_to_phone)

    def _list_thumbnail(view, context, model, name):
        if not model.avatar:
            return ''
        return Markup('<img src="%s" width="50" height="50"' % model.avatar)

    def _list_status(view, context, model, name):
        if model.status == 2:
            return '未发布'
        elif model.status == 3:
            return '待审核'
        elif model.status == 4:
            return '审核未通过'
        elif model.status == 5:
            return '运行完成'
        elif model.status == 6:
            return '完成'
        elif model.status == 7:
            return '暂停'
        elif model.status == 8:
            return '停止'

    column_formatters = {'avatar': _list_thumbnail, 'status': _list_status}
    column_extra_row_actions = [
        EndpointLinkRowAction(
            'off glyphicon glyphicon-off',
            'project.activate_project_view',
        ),
        EndpointLinkRowAction(
            'export glyphicon glyphicon-export',
            'project.project_export',
        )
    ]

    @expose('/random', methods=('GET',))
    def get_random_projects(self):
        print('test')
        return redirect(return_url)

    @expose('/export', methods=('GET',))
    def project_export(self):
        project_id = request.args["id"]
        project = get_project_satisfied(project_id)
        tasks = task_repo.get_tasks_to_export_result(project_id)
        result = []
        for task in tasks:
            if task.issue.get('image_url'):
                result.append([task.id, task.issue['image_url'], task.task_answer])
            else:
                result.append([task.id, task.issue, task.task_answer])

        name = project.name + '_' + str(project_id) + '_' + str(int(time.time()))
        path = generate_csv(name, ['task_id', 'issue', 'answer'], result)
        upload = Upload()
        url = upload.qiniu_local_upload('picture', name, path)
        return jsonify({'url': url})

    @expose('/activate/', methods=('GET',))
    def activate_project_view(self):
        """
            Activate user model view. Only GET method is allowed.
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = request.args["id"]
        model = self.get_one(id)

        if model is None:
            flash(gettext('project不存在'), 'error')
            return redirect(return_url)

        if model.status == 5:
            flash(gettext('已经审核通过， 无需重复审核.'), 'warning')
            return redirect(return_url)
        request_project_validation(id)
        flash(gettext('审核通过'), 'success')
        return redirect(return_url)

    list_template = 'project_list.html'
    details_template = 'project_details.html'

    def render(self, template, **kwargs):
        if template == 'project_details.html':
            model = kwargs['model']
            data = project_repo.get_project_statistic(model.id)
            kwargs['days'] = data['days']
            kwargs['running_data'] = data['running']
            kwargs['not_start'] = data['not_start']
            workers = {}
            # workers = {int(ele[0]): requests.get(f'http://117.50.3.122:5003/statistic/{model.id}/{int(ele[0])}/accuracy') for ele in model.workers_in_project()}
            for ele in model.workers_in_project():
                worker_id = int(ele[0])
                url = f'http://117.50.3.122:5003/statistic/{model.id}/{worker_id}/accuracy'
                resp = requests.get(url)
                if resp.status_code != 200:
                    continue
                workers[worker_id] = resp.json()['accuracy']
            kwargs['workers'] = workers
        return super(ProjectModelView, self).render(template, **kwargs)


class WorkerModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('.login_view'))
    can_view_details = True
    # column_exclude_list = ['recommend_rel', 'orientation', 'accuracy',  'access_token','deleted_at','password', ]
    column_searchable_list = ['fullname', 'id', 'phone']
    column_filters = ['id', 'fullname', 'phone', ]
    column_list = ('id', 'avatar', 'username', 'phone', 'created_at', 'ref', 'money')
    column_labels = dict(id='id', phone='手机', username='用户名', avatar='头像', created_at='创建时间', ref='来源id', money='可提现金额')
    details_template = 'worker_details.html'
    column_sortable_list = ('id', 'avatar', 'username', 'phone', 'created_at', 'ref', 'money')
    column_details_list = ['id', 'phone', 'username', 'avatar', 'created_at', 'ref', 'money']

    def render(self, template, **kwargs):
        if template == 'worker_details.html':
            model = kwargs['model']
            exchange_list = worker_withdraw_repo.get_all(worker_id=model.id)
            records = task_record_repo.get_all(worker_id=model.id)
            print(records)
            kwargs['exchange_list'] = exchange_list

            kwargs['records'] = records
        return super(WorkerModelView, self).render(template, **kwargs)

    def _list_thumbnail(view, context, model, name):
        if not model.avatar:
            return ''
        return Markup('<img src="%s" width="50" height="50"' % model.avatar)

    column_formatters = {'avatar': _list_thumbnail}

from flask_admin.contrib.sqla.filters import BaseSQLAFilter


class FilterPhoneNumber(BaseSQLAFilter):
    def apply(self, query, value, alias=None):
        worker = Worker.query.filter_by(phone=value).first()
        return query.filter(self.column == worker.id)

    def operation(self):
        return 'phone number'


class TaskRecordModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('.login_view'))
    can_create = False
    can_view_details = True
    # column_exclude_list = ['expected_income','control_count', 'round_num', 'data_type',  'refer_task_record','release_count','accuracy' ]
    column_filters = ['task_id', 'project_id', FilterPhoneNumber(TaskRecord.worker_id, 'phone number')]
    column_list = ['task_id', 'project_id', 'worker_id',  'created_at', 'updated_at', 'round_num']
    column_extra_row_actions = [
        EndpointLinkRowAction(
            'glyphicon glyphicon-zoom-in',
            'taskrecord.show_image',
        )
    ]
    # 显示的时候，讲worker_id 转化为phone
    column_labels = dict(task_id='题目ID', worker_id='Phone Number', round_num='题目轮数', updated_at='更新时间',
                         created_at='创建时间', project_id='项目ID')

    def worker_id_to_phone(view, context, model, name):
        id = model.worker_id
        worker = worker_repo.get_one(id)
        return worker.phone if worker else ''

    list_template = 'task_record_list.html'
    column_sortable_list = ('id', 'worker_id', 'project_id', 'task_id', 'status', 'created_at')

    def _list_thumbnail(view, context, model, name):
        if not model.avatar:
            return ''
        return Markup('<img src="%s" width="50" height="50"' % model.avatar)

    def _list_status(view, context, model, name):
        if model.status == 1:
            return '无状态'
        elif model.status == 2:
            return '未处理'
        elif model.status == 3:
            return '处理中'
        elif model.status == 4:
            return '完成'
        elif model.status == 5:
            return '错误'
        elif model.status == 6:
            return '冲突'

    column_formatters = {'status': _list_status, 'worker_id': worker_id_to_phone}

    @expose('/show_image/', methods=('GET',))
    def show_image(self):
        id = request.args["id"]
        model = self.get_one(id)
        instance = ImageAnnotation(model.issue['image_url'], model.info['answer'], str(model.id))
        # print(instance.export_polygon_rectangle())
        if model.template_id == 6 or model.template_id == 5:
            return Markup(
                f'<div><img src="data:image/png;base64,{instance.export_polygon_rectangle().decode()}" height=700px></div>', )
        elif model.template_id == 3:
            return Markup(
                f'<div><img src="data:image/png;base64,{instance.export_key_point().decode()}" height=700px></div>')

    @expose('/show_image/api/', methods=('GET',))
    def show_image_api(self):
        id = request.args["id"]
        model = self.get_one(id)
        instance = ImageAnnotation(model.issue['image_url'], model.info['answer'], str(model.id))
        # print(instance.export_polygon_rectangle())
        if model.template_id in (5, 6, 20):
            return instance.export_polygon_rectangle()
        elif model.template_id in (3, 9):
            return instance.export_key_point()
        elif model.template_id == 19:
            return instance.export_key_point_new()
        elif model.template_id == 21:
            return instance.export_polygon()


    def render(self, template, **kwargs):
        if template == 'task_record_details.html':
            # print(kwargs)
            record = kwargs['model']
            reviews = task_review_repo.get_all(task_record_id=record.id)
            kwargs['reviews'] = reviews
            kwargs['record_id'] = record.id
        return super(TaskRecordModelView, self).render(template, **kwargs)

    @expose('/add_review', methods=('get',))
    def record_review(self):
        print(request)
        print(request.args.get('task_record_id'))
        print(request.args.get('note'))
        task_review = TaskReview()
        task_review.note = request.args.get('note')
        task_review.task_record_id = int(request.args.get('task_record_id'))
        task_review_repo.save(task_review)
        return_url = 'http://127.0.0.1:5000/admin/taskrecord/details/?id=' + request.args.get('task_record_id')
        return redirect(return_url)

    details_template = 'task_record_details.html'


class ArbitrationModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('.login_view'))
    can_create = False
    can_view_details = True
    column_extra_row_actions = [
        EndpointLinkRowAction(
            'glyphicon glyphicon-ok',
            'taskarbitration.arbiration_pass',
        ),
        EndpointLinkRowAction(
            'glyphicon glyphicon-remove',
            'taskarbitration.arbiration_no_pass',
        )
    ]
    # 显示的时候，讲worker_id 转化为phone
    column_labels = dict(worker_id='Phone Number')

    def worker_id_to_phone(view, context, model, name):
        id = model.worker_id
        worker = worker_repo.get_one(id)
        return worker.phone

    column_formatters = {'worker_id': worker_id_to_phone}

    @expose('/pass/', methods=('GET',))
    def arbiration_pass(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = request.args["id"]
        model = self.get_one(id)

        if model is None:
            flash(gettext('提现申请不存在'), 'error')
            return redirect(return_url)

        if model.status == enums.TaskArbitrationEnum.PASS.value:
            flash(gettext('已经审核通过， 无需重复审核.'), 'warning')
            return redirect(return_url)

        # 调用startask对用户发起通知
        conn = grpc.insecure_channel(_HOST + ':' + _PORT)
        client = notify_pb2_grpc.SendNotifyStub(channel=conn)
        response = client.send_arbitration_notify(
            notify_pb2.ArbitrationData(user_id=model.worker_id, task_record_id=model.task_record_id, is_pass=True,
                                       money=0.05))
        if response.status:
            model.status = enums.TaskArbitrationEnum.PASS.value
            worker_withdraw_repo.save(model)
            flash(gettext('审核通过'), 'success')
        # url = BASE_URL+'/notify/send_withdraw_msg'
        # parms = {'user_id':model.worker_id,'money':model.money,'time':'model.created_a','is_pass':True}
        # send_post(url,parms)
        return redirect(return_url)

    @expose('/no_pass/', methods=('GET',))
    def arbiration_no_pass(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = request.args["id"]
        model = self.get_one(id)

        if model is None:
            flash(gettext('提现申请不存在'), 'error')
            return redirect(return_url)

        if model.status == enums.TaskArbitrationEnum.PASS.value:
            flash(gettext('已经审核通过， 无法变为拒绝.'), 'warning')
            return redirect(return_url)

        if model.status == enums.TaskArbitrationEnum.FAIL.value:
            flash(gettext('已经拒绝申请， 无法变更状态.'), 'warning')
            return redirect(return_url)
        model.status = enums.TaskArbitrationEnum.FAIL.value
        worker_withdraw_repo.save(model)
        flash(gettext('拒绝通过完成'), 'success')
        # 调用startask对用户发起通知
        conn = grpc.insecure_channel(_HOST + ':' + _PORT)
        client = notify_pb2_grpc.SendNotifyStub(channel=conn)
        response = client.send_arbitration_notify(
            notify_pb2.ArbitrationData(user_id=model.worker_id, task_record_id=model.task_record_id, is_pass=False,
                                       money=0.05))
        return redirect(return_url)


class TaskReviewModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('.login_view'))
    can_view_details = True


class TaskEroorwModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('.login_view'))
    can_create = False
    can_view_details = True
    column_filters = ['id', 'task_id', 'project_id']
    column_extra_row_actions = [
        EndpointLinkRowAction(
            'glyphicon glyphicon-ok',
            'taskerror.task_effacer',
        ),
    ]
    # 显示的时候，讲worker_id 转化为phone
    column_labels = dict(worker_id='Phone Number')

    def worker_id_to_phone(view, context, model, name):
        id = model.worker_id
        worker = worker_repo.get_one(id)
        return worker.phone

    column_formatters = {'worker_id': worker_id_to_phone}

    @expose('/task_effacer/', methods=('GET',))
    def task_effacer(self):
        id = request.args["id"]
        model = self.get_one(id)
        conn = grpc.insecure_channel(_HOST + ':' + _PORT)
        client = notify_pb2_grpc.SendNotifyStub(channel=conn)
        response = client.effacer_error_task(notify_pb2.TaskData(task_id=model.task_id))
        return_url = get_redirect_target() or self.get_url('.index_view')
        return redirect(return_url)


class WorkerWithdrawModeView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('.login_view'))
    can_create = False
    can_view_details = True
    column_list = ['id', 'worker_id', 'account', 'money', 'third_party', 'status']
    column_searchable_list = ['id', 'worker_id', 'sd_order', 'account', 'third_order', 'status']
    column_sortable_list = ('id', 'worker_id', 'account', 'money', 'third_party', 'status')
    column_extra_row_actions = [
        EndpointLinkRowAction(
            'glyphicon glyphicon-ok',
            'workerwithdraw.withdraw_pass',
        ),
        EndpointLinkRowAction(
            'glyphicon glyphicon-remove',
            'workerwithdraw.withdraw_no_pass',
        )
    ]
    # 显示的时候，讲worker_id 转化为phone
    column_labels = dict(worker_id='Phone Number')

    def worker_id_to_phone(view, context, model, name):
        id = model.worker_id
        worker = worker_repo.get_one(id)
        return worker.phone

    column_formatters = {'worker_id': worker_id_to_phone}

    @expose('/pass/', methods=('GET',))
    def withdraw_pass(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = request.args["id"]
        model = self.get_one(id)

        if model is None:
            flash(gettext('提现申请不存在'), 'error')
            return redirect(return_url)

        if model.status == enums.WithdrawEnum.PASSED.value:
            flash(gettext('已经审核通过， 无需重复审核.'), 'warning')
            return redirect(return_url)
        model.status = enums.WithdrawEnum.PASSED.value
        worker_withdraw_repo.save(model)
        flash(gettext('审核通过'), 'success')
        # 调用startask对用户发起通知
        conn = grpc.insecure_channel(_HOST + ':' + _PORT)
        client = notify_pb2_grpc.SendNotifyStub(channel=conn)
        response = client.send_withdraw(
            notify_pb2.Data(user_id=model.worker_id, money=model.money, time=model.created_at.strftime('%Y-%m-%d'),
                            is_pass=True, account=model.account))
        return redirect(return_url)

    @expose('/no_pass/', methods=('GET',))
    def withdraw_no_pass(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = request.args["id"]
        model = self.get_one(id)

        if model is None:
            flash(gettext('提现申请不存在'), 'error')
            return redirect(return_url)

        if model.status == enums.WithdrawEnum.PASSED.value:
            flash(gettext('已经审核通过， 无法变为拒绝.'), 'warning')
            return redirect(return_url)

        if model.status == enums.WithdrawEnum.REJECTED.value:
            flash(gettext('已经拒绝申请， 无法变更状态.'), 'warning')
            return redirect(return_url)
        model.status = enums.WithdrawEnum.REJECTED.value
        worker_withdraw_repo.save(model)
        flash(gettext('拒绝通过完成'), 'success')
        # 调用startask对用户发起通知
        conn = grpc.insecure_channel(_HOST + ':' + _PORT)
        client = notify_pb2_grpc.SendNotifyStub(channel=conn)
        response = client.send_withdraw(
            notify_pb2.Data(user_id=model.worker_id, money=model.money, time=model.created_at.strftime('%Y-%m-%d'),
                            is_pass=False, account=model.account))
        return redirect(return_url)


class RandomTasks(BaseSQLAFilter):
    cur = 1

    def apply(self, query, value, alias=None):
        if self.cur % 2 == 1:
            self.cur += 1
            self.tasks = db.session.query(query.subquery()).order_by(func.random()).limit(int(value))
            return db.session.query(self.tasks.subquery())
        else:
            self.cur += 1
            return db.session.query(func.count('*')).select_from(self.tasks.subquery())

    def operation(self):
        return 'random tasks'


class TaskModelView(ModelView):
    can_view_details = True
    column_list = ['id', 'project_id', 'updated_at', 'status', 'confidence']
    column_labels = dict(id='题目ID', project_id='项目ID', updated_at='更新时间', status='状态')
    column_filters = ['id', 'project_id', 'updated_at', 'status', RandomTasks(Task.id, 'num')]
    list_template = 'task_list.html'

    def _list_status(view, context, model, name):
        if model.status == 1:
            return '无状态'
        elif model.status == 2:
            return '未处理'
        elif model.status == 3:
            return '正在处理'
        elif model.status == 4:
            return '已结题'
        elif model.status == 5:
            return '错误'
        elif model.status == 6:
            return '冲突'

    @expose('/show_image/api/', methods=('GET',))
    def show_image_api(self):
        id = request.args["id"]
        taskrecords = TaskRecord.query.filter_by(task_id=id).order_by(TaskRecord.updated_at).all()
        if taskrecords:
            taskrecord = taskrecords[-1]
            print(taskrecord.id)
            instance = ImageAnnotation(taskrecord.issue['image_url'], taskrecord.info['answer'], str(taskrecord.id))
            # print(instance.export_polygon_rectangle())
            if taskrecord.template_id == 6 or taskrecord.template_id == 5:
                return instance.export_polygon_rectangle()
            elif taskrecord.template_id == 3:
                return instance.export_key_point()
        else:
            return ''

    column_formatters = {'status': _list_status}


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        exchange_flow_sum = worker_withdraw_repo.get_exchange_flow_sum()  # 提现总额
        workers_sum = worker_repo.workers_count()
        project_sum = project_repo.project_count()
        projects_data = project_repo.index_data()
        works_data = worker_repo.index_data()
        error_task_data = task_error_repo.index_data()
        money_sum = company_exchange_repo.money_sum()
        result = task_repo.get_tasks_analys('2018-06-07 06:53:02.921379', '2018-06-10 11:29:14.19041')
        return self.render('admin/index.html', works_data=json.dumps(works_data), error_task_data=error_task_data,
                           projects_data=json.dumps(projects_data), exchange_flow_sum=exchange_flow_sum,
                           workers_sum=workers_sum, project_sum=project_sum)

    @expose('/task_analys/', methods=('GET',))
    def task_analys(self):
        start = request.args["start"]
        end = request.args["end"]
        result = task_repo.get_tasks_analys(start, end)
        return json.dumps(result)

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return self.render('admin/login.html')

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            ds_admin = DSAdmin()

            form.populate_obj(ds_admin)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            ds_admin.password = generate_password_hash(form.password.data)
            print(ds_admin.email)
            ds_admin_repo.save(ds_admin)
            login.login_user(ds_admin)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return self.render('admin/register.html')

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class GoldenAnswerRecordModelView(ModelView):
    can_view_details = True
    column_filters = ['project_id', 'updated_at', 'id', FilterPhoneNumber(GoldenAnswerRecord.worker_id, 'phone number')]
    column_list = ['id', 'project_id', 'worker_id', 'phone', 'updated_at', 'accuracy']
    column_labels = dict(id='Golden ID', worker_id='Worker ID', project_id='Project ID', phone='Phone Number',
                         updated_at='创建时间', accuracy='准确度')


def create_app():
    app = Flask(__name__, template_folder='templates')
    init_login(app)
    admin = Admin(app, name='Dashboard', template_mode='bootstrap3', index_view=MyHomeView())
    CORS(app, supports_credentials=True)
    configure_app(app)
    setup_db(app)
    setup_sentry(app)
    admin.add_view(ProjectModelView(Project, db.session))
    admin.add_view(WorkerModelView(Worker, db.session))
    admin.add_view(TaskRecordModelView(TaskRecord, db.session))
    admin.add_view(TaskModelView(Task, db.session))
    admin.add_view(ArbitrationModelView(TaskArbitration, db.session))
    admin.add_view(TaskEroorwModelView(TaskError, db.session))
    admin.add_view(WorkerWithdrawModeView(WorkerWithdraw, db.session))
    admin.add_view(GoldenAnswerRecordModelView(GoldenAnswerRecord, db.session))
    # admin.add_view(IndexView(name='首页', endpoint='index'))
    setup_blueprints(app)

    return app


def configure_app(app):
    app.config.from_object(config.Config)
    config.Config.init_app(app)


def setup_db(app):
    """
    数据库初始化
    :param app:
    :return:
    """
    db.app = app
    db.init_app(app)


def setup_sentry(app):
    sentry.init_app(app)


def setup_blueprints(app):
    from dashboard.review.views import blueprint as review
    blueprints = [
        {'handler': review, 'url_prefix': ''}
    ]

    for bp in blueprints:
        app.register_blueprint(bp['handler'], url_prefix=bp['url_prefix'])


def generate_csv(name, header, data):
    name = uploads_path + '/' + name + '.csv'
    with open(name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)
    return name


def get_project_satisfied(project_id, **kwargs):
    """
    根据project id和允许的单个project status获取Project，如果不合法则抛出异常
    :param project_id:
    :param kwargs:
    :return:
    """
    project = project_repo.get_project_by_id(project_id)
    # for key, value in kwargs.items():
    #     if key == 'status':
    #         if getattr(project, key) == value:
    #             continue
    #         else:
    #             if value == ProjectStatusEnum.UNRELEASED.value:
    #                 raise ApiException(10002, 'The project has been released already.')
    #             elif value == ProjectStatusEnum.COMPLETED.value:
    #                 raise ApiException(10002, 'The project has not completed yet.')
    #             elif value == ProjectStatusEnum.RUNNING.value:
    #                 raise ApiException(10002, 'The project is not running.')
    #             elif value == ProjectStatusEnum.PAUSED.value:
    #                 raise ApiException(10002, 'The project is not paused.')
    #             else:
    #                 raise ApiException(10002, 'Invalid project')
    #     else:
    #         # project不存在该属性
    #         if not hasattr(project, key):
    #             raise BackendException(1000, f'Invalid attributes {key} for class project.')
    #         if getattr(project, key) == value:
    #             continue
    #         else:
    #             if key == 'company_id':
    #                 raise ApiException(10002, 'Trying to operate invalid project.')
    #             else:
    #                 raise ApiException(10002, 'Invalid project')

    return project


def request_project_validation(project_id):
    app = current_app
    startask_url = app.config['STARTASK_URL']
    url = "{}/project/{}/new_validation".format(startask_url, project_id)
    r = requests.get(url)
    print(r.text)
