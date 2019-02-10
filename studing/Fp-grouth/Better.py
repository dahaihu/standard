from functools import reduce, partial
import time
from collections import defaultdict

"""
全部都不需要headerTable
根据孩子节点的索引来进行计算

如何初始化这棵树呢？

如何递归的合并节点呢？

children 存储的是字符， 或者该字符对应的TreeNode

children 中的非节点类型，全存储为None，这样子应该会更快的
目前评测着，没有问题
因为node2往node1节点上合并的话，得是node2是一个节点，那么node1就可以从node2上来进行获取数据
这样在进行获取node_list的时候也是加快素的的
测试了isinstance(node, TreeNode)的速度比if node在进行一亿个节点的判断的时候要慢了一倍


字典通过[]获取值比get来获取值会更快

可不可以通过在mergeNode的过程中维护一个headerTable

1. 创建树的时候，创建成功。包含parent，以及headerTable
2. 计算结果有问题啊，但是实例是没有问题的，也没出bug，这他妈就很无语了
3. 上面的问题解决了，下一步试着用字典表示children？
4. 这个用字典解决，是不是就是巅峰了?
"""


# cost = 0
#
# def isinstance(a, b):
#     start = time.time()
#     res = isinstance(a, b)
#     global cost
#     cost += time.time() - start
#     return res


class TreeNode:
    # 名字，次数，父节点
    # 初始化是不是也应该传入孩子节点的长度
    def __init__(self, nameValue, parent, numOccur, children):
        self.name = nameValue  # 当前节点的名称
        self.parent = parent
        self.count = numOccur  # 当前节点在此模式下的出现次数
        self.children = children  # 当前节点的孩子节点

    def inc(self, numOccur):  # 由于事务是含有次数的，所以，当前节点出现的频次可能是多余1的，所以加上numOccur
        self.count += numOccur

    def disp(self, ind=1):
        """
        这个应该是通过“作图”(就是打印)来描述数，那么这个是如何打印的呢？拥有一个父节点的孩子，在同一层
        垂直一条线上的节点，为同一层的节点
        :param ind:
        :return:
        """
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children:
            if isinstance(child, TreeNode):
                child.disp(ind + 1)

    def __str__(self):
        return 'node is {}, node.count is {}, node.children is {}'.format(self.name, self.count,
                                                                          [node for node in self.children])


def createInitSet(dataSet):
    """
    对数据集进行统计，使用事务记录作为键，事务记录出现的次数作为值
    感觉其实并没有什么卵用
    :param dataSet:
    :return:
    """
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0) + 1
    return retDict


def getCur(node, inTree, node_to_ind):
    """
    :param node: 节点的名字
    :param inTree: 父节点
    :param mark: 通过mark获取节点的位置
    :return:
    """
    try:
        index = node_to_ind[inTree.name]
    except KeyError:
        index = -1
    return node_to_ind[node] - index - 1


# 我也来写个牛逼的算法
# mark是不是应该从大到小的排列，这样好计算些？
def updateTree(items, inTree, count, mark, ht):
    # inTree.update_desc(set(items))
    cur = getCur(items[0], inTree, mark)
    # print("index is {}".format(cur))
    # print("{}子节点的顺序为{}".format(items[0], [ele.name if isinstance(ele, TreeNode) else ele for ind, ele in enumerate(inTree.children) if ind > cur]))
    if inTree.children[cur]:
        inTree.children[cur].inc(count)
    else:
        # 初始化节点的时候，得计算孩子节点的个数
        inTree.children[cur] = TreeNode(items[0], inTree, count, [None] * (len(inTree.children) - cur - 1))
        ht.setdefault(items[0], set()).add(inTree.children[cur])
    if len(items) > 1:
        updateTree(items[1:], inTree.children[cur], count, mark, ht)


# 创建Fpgrouth-Tree
# 传入的dataSet是一个字典，键是事务，值是事务出现的次数
def createTree(dataSet, minSup=1):  # create FP-tree from dataset but don't mine
    # 需要注意的是这个headerTable是个字典
    # 首先，用来存储所有项目及其频次，然后对频次小于minSup的进行删除
    # 然后进行修改，键是频繁项，值变成一个含有两项的列表，
    # 第一项用来存储之前存储的当前频繁项的频次，
    # 第二项用来当指针，用来指向构建的树种，与该节点的nameValue相同的节点
    headerTable = {}
    # go over dataSet twice 遍历两遍数据库
    # 第一遍，统计频繁项出现的频次
    for trans in dataSet:  # first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    s = set(headerTable.keys())
    for ind in s:
        if headerTable[ind] < minSup:
            del headerTable[ind]

    # mark用来找关键字的位置的
    # 这个默认的就是从小到大排列的
    # 现在是不是应该从大到小排列的呢？
    apr = sorted(headerTable, key=lambda key: headerTable[key], reverse=True)
    print("从大到小的顺序为{}".format(apr))

    # 标准提前一下子指定，而不是每次都制定以下标准
    mark = {key: ind for ind, key in enumerate(apr)}
    # print("mark is {}".format(mark))

    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0: return None, None  # if no items meet min support -->get out

    ht = dict()

    retTree = TreeNode('Null Set', None, 1, [None] * len(apr))  # create tree
    # 怎么建树呢？
    for tranSet, count in dataSet.items():  # go through dataset 2nd time 一猜就知道dataSet是经过处理的数据集合
        localD = {}  # 这个是用来干什么的？？？用来获取当前事务中所含的频繁项集
        for item in tranSet:  # put transaction items in order
            if item in mark:
                localD[item] = mark[item]
        # localD用来存放该事务记录中，每个频繁项的频次
        if len(localD) > 0:
            # 对频繁项按照出现的次数进行从大到小的排序
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1])]
            # print("orderedItems is {}".format(orderedItems))
            ##总的应该是，对每个事物的项目，根据项目的频率，按照从大到小的排序
            updateTree(orderedItems, retTree, count, mark, ht)  # populate tree with ordered freq itemset

    return retTree, mark, ht


# 这个功能的使用，得提前创建一个节点，避免对原来的树造成混乱
# 影响的永远都是第一个节点
# 对第一个节点进行改造
# 还是有点问题的，并没有node完成初始化
# 好像并没有关联起来，仅仅对node1初始化为TreeNode，是不是没有用的
# 还是用一个字典吧
def mergeNode(headerTable, node1, node2):
    """
    把node2节点上的数据，复制到node1上去。
    但是呢当node1位
    :param retTree:
    :param node:
    :return:
    """
    node1.inc(node2.count)
    for ind, node in enumerate(node2.children):
        if node:
            if not node1.children[ind]:
                node1.children[ind] = TreeNode(node.name, node1, 0, [None] * len(node.children))
                headerTable.setdefault(node.name, set()).add(node1.children[ind])
            mergeNode(headerTable, node1.children[ind], node)
    return node1


def mergeNode_no(node1, node2, headerTable):
    """
    在node1是None的时候，如何确定node1的父节点呢？
    """
    for ind, node in enumerate(node2.children):
        if node:
            if not node1.children[ind]:
                node1.children[ind] = TreeNode(node.name, node1, 0, [None] * len(node2.children))
                headerTable[node.name].add(node1.children[ind])

            headerTable[node.name].remove(node)
            node1.children[ind].inc(node.count)
            mergeNode_no(node1.children[ind], node, headerTable)
    return node1


# 这个地方更新的时候，是不是还得应该更新一下headerTable
def update2(node, node_to_ind, headerTable):
    # 获取节点node在父节点的children中的索引
    index = getCur(node.name, node.parent, node_to_ind)
    for ind, child in enumerate(node.children):
        if child:
            # 要对headerTable进行更新
            # 新添加的节点要加到headerTable中对应的集合中去
            # 而对合并的节点，child，则要从headerTable中移除
            if not node.parent.children[ind + 1 + index]:
                node.parent.children[ind + 1 + index] = TreeNode(child.name, node.parent, 0,
                                                                 [None] * len(child.children))
                headerTable[child.name].add(node.parent.children[ind + 1 + index])
            # mergeNode_no的时候，并没有对headerTable进行更新，所以造成了结果的错误？
            node.parent.children[ind + 1 + index].inc(child.count)
            headerTable[child.name].remove(child)
            mergeNode_no(node.parent.children[ind + 1 + index], child, headerTable)
    node.parent.children[index] = None


"""
现在mineTree和节点的descendants没有关系了
而是通过对headerTable来进行操作
"""


def mineTree(inTree, minSup, prefix, ind_to_node, node_to_ind, headerTable, res):
    """
    :param inTree:
    :param minSup:
    :param prefix:
    :param res:
    :return:
    """
    headerList = sorted(headerTable, key=lambda x: node_to_ind[x], reverse=True)
    # print("headerList is {}".format(headerList))
    for header in headerList:
        node_list = headerTable[header]
        count = reduce(lambda x, y: x + y.count, node_list, 0)
        if count < minSup:
            for node in node_list:
                update2(node, node_to_ind, headerTable)
        else:
            """
            照理说，这个else语句中的情况下
            node这棵树是不应该有inTree这棵树中的非频繁节点的
            """
            res.append(prefix + [header])
            print("new frequent item sets is {}".format(prefix + [header]))
            node = TreeNode(header, inTree, 0, [None] * (len(ind_to_node) - node_to_ind[header] - 1))
            ht = dict()
            custom_merge = partial(mergeNode, ht)
            reduce(custom_merge, node_list, node)
            # print("prefix is {}".format(prefix + [node.name]))
            # for key, value in ht.items():
            #     print("{} => {}".format(key, value))
            # node.disp()
            mineTree(node, minSup, prefix + [node.name], ind_to_node, node_to_ind, ht, res)


def loadDataset(path, _max=float('inf')):
    dataset = []
    with open(path, 'r') as file:
        count = 0
        for line in file:
            count += 1
            # print(line.strip().split(' '))
            dataset.append(line.strip().split(' '))
            if count >= _max:
                break
    minSup = len(dataset) * 0.2
    return minSup, dataset


# 测试删除支持度小于最小支持度的节点
def test_update():
    pass


# 感觉是有戏的，啊哈哈，啊哈哈，这几天放假还是有收获的
def final_test():
    import time
    start = time.time()
    minSup, dataset = loadDataset(r'/Users/hushichang/mushroom.dat.txt')
    retDict = createInitSet(dataset)
    retTree, node_to_ind, headerTable = createTree(retDict, minSup)
    ind_to_node = {value: key for key, value in node_to_ind.items()}
    retTree.disp()
    res = []
    mineTree(retTree, minSup, [], ind_to_node, node_to_ind, headerTable, res)
    print("length is {}".format(len(res)))
    # for line in res:
    #     print(line)
    print("cost time is {}".format(time.time() - start))


def test_function():
    start = time.time()
    # dataset = [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]
    # dataset = [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5']]
    # dataset = [['bread', 'milk', 'vegetable', 'fruit', 'eggs'],
    #            ['noodle', 'beef', 'pork', 'water', 'socks', 'gloves', 'shoes', 'rice'],
    #            ['socks', 'gloves'],
    #            ['bread', 'milk', 'shoes', 'socks', 'eggs'],
    #            ['socks', 'shoes', 'sweater', 'cap', 'milk', 'vegetable', 'gloves'],
    #            ['eggs', 'bread', 'milk', 'fish', 'crab', 'shrimp', 'rice']]
    dataset = [[1, 2, 5], [2, 4], [2, 3], [1, 2, 4], [1, 3], [2, 3], [1, 3], [1, 2, 3, 5], [1, 2, 3]]
    minSup = 3
    retDict = createInitSet(dataset)
    # for key, value in retDict.items():
    #     print("{} => {}".format(key, value))
    retTree, node_to_ind, headerTable = createTree(retDict, minSup)
    retTree.disp()
    # for node in headerTable['5']:
    #     update2(node, node_to_ind)
    ind_to_node = {value: key for key, value in node_to_ind.items()}
    #
    result = []
    mineTree(retTree, minSup, [], ind_to_node, node_to_ind, headerTable, result)
    print("length is {}".format(len(result)))
    for res in result:
        print(res)
    #
    # print("cost is {}".format(time.time() - start))


def test_update():
    dataset = [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]
    # dataset = [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5']]
    # dataset = [['bread', 'milk', 'vegetable', 'fruit', 'eggs'],
    #            ['noodle', 'beef', 'pork', 'water', 'socks', 'gloves', 'shoes', 'rice'],
    #            ['socks', 'gloves'],
    #            ['bread', 'milk', 'shoes', 'socks', 'eggs'],
    #            ['socks', 'shoes', 'sweater', 'cap', 'milk', 'vegetable', 'gloves'],
    #            ['eggs', 'bread', 'milk', 'fish', 'crab', 'shrimp', 'rice']]
    # dataset = [[1,2,5],[2,4],[2,3],[1,2,4],[1,3],[2,3],[1,3],[1,2,3,5],[1,2,3]]
    minSup = 2
    retDict = createInitSet(dataset)
    # for key, value in retDict.items():
    #     print("{} => {}".format(key, value))
    retTree = createTree(retDict, minSup=minSup)
    retTree.disp()
    update(retTree, 1)
    retTree.disp()
    print(retTree.children)
    # print(retTree.children[1].children)
    # print(retTree.children[0].children[0].children[1])
    # result = []
    # mineTree(retTree, minSup, [], result)
    # print("length is {}".format(len(result)))
    # for res in result:
    #     print(res)


if __name__ == '__main__':
    final_test()
    # test_function()
    # test_update()
