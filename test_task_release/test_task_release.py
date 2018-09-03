from stardust.core import create_app
from flask import jsonify
import pytest
from flask import Response
from flask import url_for
import json

import os
import tempfile

import pytest






@pytest.fixture
def app():
    app = create_app()
    # app.response_class = MyResponse
    # app.run()
    return app


@pytest.fixture
def client(app):
    test_client = app.test_client()

    # def teardown():
    #     pass
    #
    # request.addfinalizer(teardown)
    return test_client


# class MyResponse(Response):
#     @property
#     def json(self):
#         return 42

d = {
  "phone": "17667935786",
  "password": "hscxrzs1st"
}

# 第一个测试用例是完全正确的
def test_task_release1(client):
    res = client.get('task/release?project_id=66', headers={"Authorization":"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MzU1ODQ5MDYsImlhdCI6MTUzNTU4NDkwNSwiaXNzIjoia2VuIiwiZGF0YSI6eyJ3b3JrZXJfaWQiOjMzLCJsb2dpbl9hdCI6MTUzNTU4NDkwNX19.K4Q3yAMK71pV_T2GL2vMBEqv3RDp76XGim6wvdU2SCk"})
    data = json.loads(res.data)
    assert not data.get('err_code')

# 第二个错误用例是项目id是有问题的
def test_task_release2(client):
    res = client.get('task/release?project_id=1000', headers={"Authorization":"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MzU1ODQ5MDYsImlhdCI6MTUzNTU4NDkwNSwiaXNzIjoia2VuIiwiZGF0YSI6eyJ3b3JrZXJfaWQiOjMzLCJsb2dpbl9hdCI6MTUzNTU4NDkwNX19.K4Q3yAMK71pV_T2GL2vMBEqv3RDp76XGim6wvdU2SCk"})
    data = json.loads(res.data)
    assert not data.get('err_code')



# 第三个错误用例是项目是headers中没有authorization
def test_task_release3(client):
    res = client.get('task/release?project_id=1000')
    data = json.loads(res.data)
    assert not data.get('err_code')


# 第四个错误用例是项目id是有问题的头部信息中的jwt有问题
def test_task_release4(client):
    res = client.get('task/release?project_id=1000', headers={"Authorization":"JWT eyJ0eXAiiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MzU1ODQ5MDYsImlhdCI6MTUzNTU4NDkwNSwiaXNzIjoia2VuIiwiZGF0YSI6eyJ3b3JrZXJfaWQiOjMzLCJsb2dpbl9hdCI6MTUzNTU4NDkwNX19.K4Q3yAMK71pV_T2GL2vMBEqv3RDp76XGim6wvdU2SCk"})
    data = json.loads(res.data)
    assert not data.get('err_code')
