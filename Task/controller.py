# -*- coding: utf8 -*-
from typing import List

from stardust_v4.model import user_repo, container_repo, TaskHistory, task_history_repo


def _get_task_record(task_id: int) -> List[TaskHistory]:
    """
    根据task_id查询到历史记录，并返回
    :param task_id:
    :return:
    """
    records = task_history_repo.get_all(id=task_id)
    for task_record in records:
        # 根据user_id查找user，并获取user的相关信息
        user_id = task_record.user_id
        user = user_repo.get_one(user_id)
        # 17767196163 变为 177****6163
        task_record['phone'] = user.phone[:3] + '****' + user.phone[-4:]
        task_record['username'] = user.name

        # 根据container_id 获取container的信息
        container = container_repo.get_one(task_record.container_id)
        task_record['container_name'] = container.name

        # 根据task_record设定相关信息
        task_record['timestamp'] = task_record.updated_at
        task_record['action'] = task_record.result
        task_record['comment'] = task_record.comment

        # task_record_proto = dict_to_proto(TaskHistoryProto, task_record)

    return records
