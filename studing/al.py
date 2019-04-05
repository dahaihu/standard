# a = [(1, 2), (2, 5), (6, 9), (9.5, 20)]
# b = [(1.5, 2.5), (3, 10)]
a = [(1, 3), (5, 6)]
b = [(0, 1), (2, 5), (7, 8)]
import json
import time
import string
from collections import defaultdict

def func(a, b):
    a.extend(b)
    a.sort(key=lambda x: x[0])
    # print(a)
    inter = 0
    union = 0
    # 长度为1 就不需要计算了
    # 但是传入的参数a, b都不会为空
    if len(a) <= 1:
        return
    # print("len(a) is {}".format(len(a)))
    i, j = 0, 1
    while i <= len(a)-1 and j <= len(a) - 1:
        # print("i is {}, j is {}".format(i, j))
        if a[i][1] <= a[j][0]:
            union += a[i][1] - a[i][0]
            i, j = j, j+1
            # print("*")
            # print("{} => {}".format(i, j))
            continue
        elif a[i][1] > a[j][0]:
            if a[i][1] <= a[j][1]:
                union += a[i][1] - a[i][0]
                inter += a[i][1] - a[j][0]
                a[j] = (a[i][1], a[j][1])
                i, j = j, j+1
                # print("**")
                # print("union is {}".format(union))
                # print('inter is {}'.format(inter))
                # print("{} => {}".format(i, j))
                # print("a[i] is {}".format(a[i]))
            else:
                inter += a[j][1] - a[j][0]
                union += a[j][1] - a[i][0]
                a[i] = (a[j][1], a[i][1])
                i, j = i, j+1
    #             print("***")
    #             print("union is {}".format(union))
    #             print('inter is {}'.format(inter))
    #             print("{} => {}".format(i, j))
    #             print("a[i] is {}".format(a[i]))
    # print("i is {}".format(i))
    # print("j is {}".format(j))
    if i <= len(a)-1:
        union += a[i][1] - a[i][0]
    if j <= len(a) - 1:
        union += a[j][1] - a[j][0]
    return inter/union
    # print(f'intersection:{inter}, union:{union}')
    # # union += a[-1][1] - a[-1][0]
    # print("a[-1] is {}".format(a[-1]))
    # print('union {}'.format(union))
    # print('inter {}'.format(inter))


def _audio_data_transfer(data):
    """
    语音转文本数据格式处理，格式示例：
    [{"from": 0.5224489795918363, "index": 0, "text": "hello~~~", "to": 1.5557369614512475},
    {"from": 2.443900226757368, "index": 1, "text": "world", "to": 3.5236281179138307}]
    :param args:
    :return:
    """
    if not data or type(data) != list:
        raise Exception

    data.sort(key=lambda x: x.get('from'))
    trans = defaultdict(list)

    for anno in data:
        start = anno.get('from', None)
        if start is None:
            raise Exception
        start = round(float(start), 2)

        end = anno.get('to', None)
        if end is None:
            raise Exception
        end = round(float(end), 2)

        if start >= end:
            raise Exception
        if not trans['time_iou']:
            trans['time_iou'].append((start, end))
        else:
            last = trans['time_iou'][-1][1]  # 新的start必须大于最后一个end
            if end < last:  # 如果新的end小于最后一个end，则忽略这个标注时间
                pass
            elif start < last:  # 如果新的start小于最后一个end，则新的start等于最后一个end
                start = last
                trans['time_iou'].append((start, end))
            else:
                trans['time_iou'].append((start, end))

        text = anno.get('text', None)
        if text is None:
            raise Exception
        text = ''.join(ch for ch in text if ch not in set(string.punctuation))
        trans['text_anno'] += text

    return trans



def _audio_time_iou(pre_time, post_time):
    """
    音频转文本的时间相似度，iou代表intersection over union
    :param pre_time: [(start time, end time) ...]
    :param post_time: [(start time, end time) ...]
    :return:
    """

    def _time_next(time_sequence, cur=None):
        """
        获取下一个pointer
        :param time_sequence: 传入要找到指针的time sequence
        :param cur: 当前指针位置，例如(0,0)，第一个数字代表list的index，第二个数字代表tuple的index
        :return: pointer_time, list_index, tuple_index
        """
        if cur is None:
            # print(time_sequence)
            return time_sequence[0][0], (0, 0)
        list_pos = cur[0]
        tuple_pos = cur[1]
        if tuple_pos == 0:
            return time_sequence[list_pos][1], (list_pos, 1)
        elif list_pos != len(time_sequence) - 1:
            return time_sequence[list_pos + 1][0], (list_pos + 1, 0)
        else:
            return None, None

    time_counter, counter = [], 0
    pre_cur, pre_seq = _time_next(pre_time)
    post_cur, post_seq = _time_next(post_time)

    def _time_counter(cur, seq, cur_time):
        nonlocal counter, time_counter
        counter = counter + 1 if not seq[1] else counter - 1
        time_counter.append((cur, counter))
        return _time_next(cur_time, seq)

    while pre_cur is not None or post_cur is not None:
        if pre_cur is not None and post_cur is not None:
            if pre_cur <= post_cur:
                pre_cur, pre_seq = _time_counter(pre_cur, pre_seq, pre_time)
            else:
                post_cur, post_seq = _time_counter(post_cur, post_seq, post_time)
        elif pre_cur:
            pre_cur, pre_seq = _time_counter(pre_cur, pre_seq, pre_time)
        else:
            post_cur, post_seq = _time_counter(post_cur, post_seq, post_time)

    # print(f'time_counter:{time_counter}')

    union, intersection = 0, 0
    for index, e in enumerate(time_counter):
        if e[1] == 1:  # 两个集合只有一个
            union += time_counter[index + 1][0] - e[0]
        elif e[1] == 2:  # 两个集合都有
            intersection += time_counter[index + 1][0] - e[0]

    # print(f'intersection:{intersection}, union:{union + intersection}')

    return intersection / (union + intersection)

#
# #
start = time.time()
with open("CompleteBinary.py.json", 'r') as file:
    content = json.load(file)
    for ind, ele in enumerate(content):
        pre = ele.get('pre')
        pre_res = _audio_data_transfer(pre).get('time_iou')
        post = ele.get('post')
        # post_res = []
        # for data in post:
        #     post_res.append((data.get('from'), data.get('to')))
        post_res = _audio_data_transfer(post).get("time_iou")

        pre_res.sort(key=lambda x: x[0])
        post_res.sort(key=lambda x: x[0])
        print("ind is {}".format(ind))
        print("pre_res length {}".format(len(pre_res)))
        print("post_res length {}".format(len(post_res)))
        # if ind == 0:
        #     print(pre_res)
        #     print(post_res)
        print("************")
        print(_audio_time_iou(pre_res, post_res))
        # print(func(pre_res, post_res))
print(time.time()-start)


# import copy
# import random
# pre_demo = []
# pre_d = dict().fromkeys(['from', 'index', 'text', 'to'])
# i = 0
# while i < 5000000:
#     tmpd = copy.deepcopy(pre_d)
#     tmpd['from'] = random.uniform(i, i + 5)
#     z = random.uniform(tmpd['from']+0.01, tmpd['from'] + 5)
#     tmpd['to'] = random.uniform(tmpd['from']+0.01, z)
#     tmpd['text'] = "填,空"
#     i = z
#     pre_demo.append(tmpd)
#
# post_demo = []
# i = 0
# while i < 5000000:
#     tmpd = copy.deepcopy(pre_d)
#     tmpd['from'] = random.uniform(i, i + 5)
#     z = random.uniform(tmpd['from']+0.01, tmpd['from'] + 5)
#     tmpd['to'] = random.uniform(tmpd['from'] + 0.01, z)
#     tmpd['text'] = "填,空"
#     i = z
#     post_demo.append(tmpd)
#
# res = []
# res.append({"pre":pre_demo, 'post':post_demo})
# with open("CompleteBinary.py.json", 'w') as file:
#     json.dump(res, file)