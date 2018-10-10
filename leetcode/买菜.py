# value = input().split(r'\n')
# # 获取有多少份菜，和满减的条件
# n, X = [int(ele) for ele in value[0].split(' ')]
# costList = [int(ele) for ele in value[1].split(' ')]
# # print(n, X, costList)


# costList = [18, 19, 17, 6, 7]
# res = [0]
# for ele in costList:
#     num = len(res)
#     for i in range(num):
#         if res[i] > 20:
#             continue
#         else:
#             res.append(res[i] + ele)
# print(res)
# mn = float('inf')
#
# for ele in res:
#     if ele < 20:
#         continue
#     else:
#         mn = ele if ele < mn else mn
# print(mn)

costList = [18, 19, 17, 6, 7]
X = 20
costList.sort()
res = []
mn = float('inf')
for ind, ele in enumerate(costList):
    tmp_res = ele
    left, right = ind
