# -*- coding: utf8 -*-

from flask import Blueprint, request, jsonify

from shared_models.generated.python.task_v4_pb2 import TaskHistoryProto, ListTaskHistoriesResponseProto, \
    ListTaskHistoriesRequestProto
from stardust_v4.Task import controller
from stardust_v4.utility.api_check import variable_check, ResponseCodeEnum
from stardust_v4.user.enum import RoleEnum
from stardust_v4.auth.permission import auth_control
from stardust_v4.data_factory.protobuf import dict_to_proto, proto_to_dict

blueprint = Blueprint('task', __name__)


@blueprint.route('', methods=["GET"])
@auth_control([RoleEnum.DEFAULT])
def get_task_history():
    # 处理请求参数
    req_dict = eval(request.args['pb'])
    required = {'task_id'}
    variable_check(req_dict, required)
    req_proto = dict_to_proto(ListTaskHistoriesRequestProto, req_dict)
    task_id = req_proto.id

    task_records = controller._get_task_record(task_id)

    res = []
    for task_record in task_records:
        task_record_dict = task_record.to_dict()
        task_record_proto = dict_to_proto(TaskHistoryProto, task_record_dict)
        res.append(task_record_proto)

    task_records_proto = ListTaskHistoriesResponseProto()
    task_records_proto.histories.extend(res)

    rep = proto_to_dict(task_records_proto)
    return jsonify(status=dict(code=ResponseCodeEnum.OK.value), response=rep)
