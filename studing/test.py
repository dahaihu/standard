import copy
import random
import json
res = []
pre_demo = []
pre_d = dict().fromkeys(['from', 'index', 'text', 'to'])
for i in range(1000):
    tmpd = copy.deepcopy(pre_d)
    tmpd['from'] = random.uniform(i, i + 0.5)
    tmpd['to'] = random.uniform(i + 0.51, i + 1)
    tmpd['text'] = "填,空"
    pre_demo.append(tmpd)

post_demo = []
post_d = dict().fromkeys(['from', 'index', 'text', 'to'])
for i in range(1000):
    tmpd = copy.deepcopy(pre_d)
    tmpd['from'] = i
    tmpd['to'] = i + 1
    tmpd['text'] = "填,空"

    post_demo.append(tmpd)
res.append({"pre":pre_demo, 'post':post_demo})
with open('CompleteBinary.py.json', 'w') as file:
    json.dump(res, file)
