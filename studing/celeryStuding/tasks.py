from celery import Celery
from celery import Task
from celery.utils.log import get_task_logger
app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

#
# class MyTask(Task):
#     def on_success(self, retval, task_id, args, kwargs):
#         print("task done:{0}".format(retval))
#         return super(MyTask, self).on_success(retval, task_id, args, kwargs)
#
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         print('task fail, reason: {0}'.format(exc))
#         return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)
#
#
#
# @app.task(base=MyTask)
# def add(x, y):
#     raise KeyError
#     return x + y


# logger = get_task_logger(__name__)
# @app.task(bind=True)
# def add(self, a, b):
#     logger.info(self.request.__dict__)
#     return a + b



app.config_from_object('celery_config')

@app.task(bind=True)
def period_task(self):
    print('period task done: {0}'.format(self.request.id))