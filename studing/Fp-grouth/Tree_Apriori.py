from functools import reduce, partial
import time
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
    def __init__(self, nameValue, parent, numOccur):
        self.name = nameValue  # 当前节点的名称
        self.parent = parent
        self.count = numOccur  # 当前节点在此模式下的出现次数
        self.children = dict()  # children用字典来表示

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
        for child in self.children.values():
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


# 我也来写个牛逼的算法
# mark是不是应该从大到小的排列，这样好计算些？
def updateTree(items, inTree, count, mark, ht):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        # 初始化节点的时候，得计算孩子节点的个数
        inTree.children[items[0]] = TreeNode(items[0], inTree, count)
        ht.setdefault(items[0], set()).add(inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1:], inTree.children[items[0]], count, mark, ht)


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

    retTree = TreeNode('Null Set', None, 1)  # create tree
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


"""
三个函数的功能，基本相似
可不可以合并？
似乎还能改进？合并一棵子树的时候，根节点是不是不用inc(count)。加上了也并不会使用。
"""
def mergeNode(headerTable, node1, node2):
    """
    把node2节点上的数据，复制到node1上去。
    但是呢当node1位
    :param retTree:
    :param node:
    :return:
    """
    node1.inc(node2.count)
    for name, child in node2.children.items():
        if name not in node1.children:
            node1.children[name] = TreeNode(name, node1, 0)
            headerTable.setdefault(name, set()).add(node1.children[name])
        mergeNode(headerTable, node1.children[name], child)
    return node1

"""
去掉非频繁节点
"""
def update(node1, node2, headerTable):
    """
    作用是合并node1和node2的子节点
    :param node1:
    :param node2:
    :param headerTable:
    :return:
    """
    for name, child in node2.children.items():
        if name not in node1.children:
            node1.children[name] = TreeNode(name, node1, 0)
            headerTable[name].add(node1.children[name])

        node1.children[name].inc(child.count)
        headerTable[name].remove(child)
        update(node1.children[name], child, headerTable)

"""
现在mineTree和节点的descendants没有关系了
而是通过对headerTable来进行操作
"""


def mineTree(inTree, minSup, prefix, node_to_ind, headerTable, res):
    """
    :param inTree:
    :param minSup:
    :param prefix:
    :param res:
    :return:
    """
    # inTree.disp()
    headerList = sorted(headerTable, key=lambda x: node_to_ind[x], reverse=True)
    # _all = set()
    # print("headerList is {}".format(headerList))
    for header in headerList:
        node_list = headerTable[header]
        count = reduce(lambda x, y: x + y.count, node_list, 0)
        if count < minSup:
            # print("node_list's length is {}".format(len(node_list)))
            # print("count is {}".format(count))
            for node in node_list:
                update(node.parent, node, headerTable)
                del node.parent.children[node.name]
        else:
            """
            照理说，这个else语句中的情况下
            node这棵树是不应该有inTree这棵树中的非频繁节点的
            """
            res.append(prefix + [header])
            print("newFreqSet is {}".format(prefix + [header]))
            node = TreeNode(header, inTree, 0)
            ht = dict()
            # 这个地方是不是得遍历一次
            # 然后mineTree的时候也得遍历一次
            custom_merge = partial(mergeNode, ht)
            reduce(custom_merge, node_list, node)
            if ht:
                # ht = {key: value for key, value in ht.items() if key not in _all}
                mineTree(node, minSup, prefix + [node.name], node_to_ind, ht, res)


def loadDataset(path, minSup):
    dataset = []
    with open(path, 'r') as file:
        count = 0
        for line in file:
            count += 1
            # print(line.strip().split(' '))
            dataset.append(line.strip().split(' '))
    minSup = len(dataset) * minSup
    return minSup, dataset


# 测试删除支持度小于最小支持度的节点
def test_update():
    pass


def bet_test(path, minSup):
    import time
    start = time.time()
    minSup, dataset = loadDataset(path, minSup)
    retDict = createInitSet(dataset)
    retTree, node_to_ind, headerTable = createTree(retDict, minSup)
    # ind_to_node = {value: key for key, value in node_to_ind.items()}
    retTree.disp()
    res = []
    # res = []
    mineTree(retTree, minSup, [], node_to_ind, headerTable, res)
    print("length is {}".format(len(res)))
    print("cost time is {}".format(time.time() - start))


def test_function():
    start = time.time()
    # dataset = [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]
    dataset = [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5'], ['1', '2', '3']]
    # dataset = [['bread', 'milk', 'vegetable', 'fruit', 'eggs'],
    #            ['noodle', 'beef', 'pork', 'water', 'socks', 'gloves', 'shoes', 'rice'],
    #            ['socks', 'gloves'],
    #            ['bread', 'milk', 'shoes', 'socks', 'eggs'],
    #            ['socks', 'shoes', 'sweater', 'cap', 'milk', 'vegetable', 'gloves'],
    #            ['eggs', 'bread', 'milk', 'fish', 'crab', 'shrimp', 'rice']]
    # dataset = [[1, 2, 5], [2, 4], [2, 3], [1, 2, 4], [1, 3], [2, 3], [1, 3], [1, 2, 3, 5], [1, 2, 3]]
    minSup = 2
    retDict = createInitSet(dataset)
    # for key, value in retDict.items():
    #     print("{} => {}".format(key, value))
    retTree, node_to_ind, headerTable = createTree(retDict, minSup)
    retTree.disp()
    # for node in headerTable['5']:
    #     update2(node, node_to_ind)
    #
    print("node_to_ind is {}".format(node_to_ind))
    print("list is {}".format(list(node_to_ind)))
    result = []
    mineTree(retTree, minSup, [], node_to_ind, headerTable, result)
    print("length is {}".format(len(result)))
    # for res in result:
    #     print(res)

# Better is the Best
# 所谓的Tree-Apriori算法
if __name__ == '__main__':
    # path = r'/Users/hushichang/Downloads/pumsb.dat'
    # path = r'/Users/hushichang/mushroom.dat.txt'
    path = r'/Users/hushichang/chess.dat'
    minSup = 0.6
    bet_test(path, minSup)
    # test_function()
    # test_update()
