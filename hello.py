projectview中添加
@action("导出这些项目下的worker完成题目的数据统计", "导出这些项目下的worker完成题目的数据统计", "haha")
def func(self, ids):
    # 获取所有的workers
    workers = set()
    for i in ids:
        # self.get_one(i) 返回的是一个project
        for ele in self.get_one(i).workers_in_project():
            workers.update(set(ele))
    # 所有项目id，类型转化为整型
    project_ids = [int(i) for i in ids]
    # 根据worker_id设置一个字典，默认值是0，用来统计worker的在这些项目下的做题结果
    result = {worker: task_record_repo.count_worker_completion_in_project_list(worker, project_ids) for worker in workers}

    return str(result)



task_record中添加
def count_worker_completion_in_project_list(self, worker_id, project_list):
    tasks_completed = rectangles_completed = 0
    sql = f"""select info->>'answer' from sd_task_record where worker_id={worker_id} and project_id in {tuple(project_list)}"""
    result = self.db.session.execute(sql)
    for ele in result:
        # 数据库里面的坐标值，有的竟然是null，这个就有点无语了
        ele = eval(ele[0].replace('null', '1'))
        # print('type(ele) is {}'.format(type(eval(ele))))
        # print('ele is {}'.format(eval(ele)))
        rectangles_completed += len(ele)
        tasks_completed += 1
        for e in ele:
            print('answer is {}'.format(e))
    return tasks_completed, rectangles_completed


a_model下的project中添加
def workers_in_project(self):
    """
    返回答过该项目下的所有woker
    :return:
    """
    sql = f"""select DISTINCT worker_id from sd_task_record where project_id = {self.id}"""
    result = db.session.execute(sql)
    return result