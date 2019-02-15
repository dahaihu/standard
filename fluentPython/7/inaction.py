import logging as logger
import requests

db_base_url = 'http://10.10.108.115:9000/api/namespaces/%s' % 'auto_data'



def http_status(resp):
    if resp.status_code / 100 == 2:
        return True
    return False

class FileClient:
    def __init__(self, base_url=db_base_url):
        self.base_url = base_url

    def create(self, dataset_name, file_name, file_uri, file_hash='',
               type='pack', tags={}, channel='', file_size=100,
               predicted=False, sliced=False, device_id='',
               belong_to='', ts=''):

        if len(tags.keys()) > 0:
            tagged = True
        else:
            tagged = False
        # TODO tag lower case

        file_post_url = '/files'
        file_post_body = {"hash": file_hash,  # MD5值
                          "uri": file_uri,  # 文件路径
                          "name": file_name,  # 文件名
                          "size": file_size,  # 文件大小
                          "type": type,  # 文件类型 jpg/pack/gpx等
                          "dataset_name": dataset_name,
                          "meta": {
                              "tags": tags,  # 自定义tag, 为一个json。标记天气时间场景等信息
                              "channel": channel,  # 摄像头组（一台车上一般有三组, front, side, fisheye之类的）
                              "tagged": tagged,  # 是否已经标记tag
                              "predicted": predicted,  # 是否已经被模型预测
                              "sliced": sliced,  # 是否已经记录pack中的数据信息
                              "device_id": device_id,  # 采集的设备号
                              "belong_to": belong_to,  # 一个自定义的组的概念, 一个组包括一个pack, 和摄像头个数相同的4/5/6张图片以及一个gpx文件。
                              "timestamp": ts  # 文件的时间戳“201803021123”
                          }}
        ret = requests.post(self.base_url + file_post_url, json=file_post_body)

        if http_status(ret):
            return json.loads(ret.content)['id']
        else:
            logger.warn(ret.content)
            return None

    def delete(self, file_id, dataset_name):
        file_delete_url = '/files/id/%s' % file_id
        resp = requests.delete(self.base_url + file_delete_url)
        if http_status(resp):
            logger.warn('delete file success')
        else:
            logger.warn('delete file failed ' + resp.text)

    def overwrite(self, file_id, file_name='', file_uri='', file_hash='',
                  type='pack', file_size=100, tags={}, channel='',
                  predicted=False, sliced=False, device_id='',
                  belong_to='', ts=''):

        if len(tags.keys()) > 0:
            tagged = True
        else:
            tagged = False

        file_put_url = '/files/id/%s' % file_id
        file_put_body = {"name": file_name,
                         "uri": file_uri,
                         "hash": file_hash,
                         "type": type,
                         "size": file_size,
                         "meta": {
                             "tags": tags,
                             "channel": channel,
                             "tagged": tagged,
                             "predicted": predicted,
                             "sliced": sliced,
                             "device_id": device_id,
                             "belong_to": belong_to,
                             "timestamp": ts
                         }}

        resp = requests.put(self.base_url + file_put_url, json={'op': "overwrite", "data": file_put_body})
        if http_status(resp):
            logger.warn('overwrite file success')
        else:
            logger.warn('overwrite file failed' + resp.text)

    def update(self, file_id, file_name=None, file_uri=None, file_hash=None,
               type=None, file_size=None, tags=None, channel=None,
               predicted=None, sliced=None, device_id=None,
               belong_to='', ts=None):

        if len(tags.keys()) > 0:
            tagged = True
        else:
            tagged = False

        file_put_url = '/files/id/%s' % file_id
        file_set_body = {
            "meta": {}
        }

        if file_name:
            file_set_body['name'] = file_name
        if file_uri:
            file_set_body['uri'] = file_uri
        if file_hash:
            file_set_body['hash'] = file_hash
        if type:
            file_set_body['type'] = type
        if file_size:
            file_set_body['size'] = file_size

        if tags:
            file_set_body['meta']['tags'] = tags
        if channel:
            file_set_body['meta']['channel'] = channel
        if tagged:
            file_set_body['meta']['tagged'] = tagged
        if predicted:
            file_set_body['meta']['predicted'] = predicted
        if sliced:
            file_set_body['meta']['sliced'] = sliced
        if device_id:
            file_set_body['meta']['device_id'] = device_id
        if belong_to:
            file_set_body['meta']['belong_to'] = belong_to
        if ts:
            file_set_body['meta']['timestamp'] = ts
        if not (tags or channel or tagged or predicted or sliced or device_id or belong_to or ts):
            file_set_body.pop('meta', None)

        # explain: http://apistore.hobot.cc/project/269/interface/api/6010
        resp = requests.put(self.base_url + file_put_url, json={'op': "patch", "data": {"set": file_set_body}})
        if http_status(resp):
            logger.warn('update file success')
        else:
            logger.warn('update file failed ' + resp.text)

    def get(self, file_id):
        dataset_get_url = '/files/id/%s' % (file_id)
        resp = requests.get(self.base_url + dataset_get_url)
        if http_status(resp):
            return resp.json()
        else:
            logger.warn('get file failed' + resp.text)

    def list(self, page=1, page_size=20):
        file_get_url = '/files?PageSize=%d&PageNo=%d' % (page_size, page)
        ret = requests.get(self.base_url + file_get_url)
        if http_status(ret):
            return ret.json()
        else:
            logger.warn('list files failed' + ret.text)

    def list_by_dataset(self, dataset, page=1, page_size=10):
        file_get_url = '/datasets/%s/files?PageSize=%d&PageNo=%d' % (dataset, 10, 1)
        ret = requests.get(self.base_url + file_get_url)
        total = ret.json()['total_count']
        from concurrent import futures
        import math
        nums = int(math.ceil(float(total) // 1000))
        with futures.ThreadPoolExecutor(nums) as executor:
            http_contents = executor.map(http_request, [
                (self.base_url + '/datasets/{}/files?PageSize={}&PageNo={}'.format(dataset, 1000, i)) for i in
                range(1, nums + 1)])
        res = []
        for http_content in http_contents:
            res.append(http_content.json()['data'])
        return res

def http_request(url):
    return requests.get(url)


fcli = FileClient()
res = fcli.list_by_dataset('20181121')
