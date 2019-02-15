from functools import reduce
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
    def __init__(self, nameValue, numOccur, children):
        self.name = nameValue  # 当前节点的名称
        self.count = numOccur  # 当前节点在此模式下的出现次数
        # 孩子节点是有序的，纯节点
        # 如果该孩子节点的count为0，也没事，但是呢，必须存在
        # self.children = [None for _ in range(llen)]  # 当前节点的孩子节点
        self.children = children  # 当前节点的孩子节点
        # 用来保存一个节点的所有子孙节点
        self.descendants = set()
        self.length = len(children)
        # self.nodes = {}

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

    # 这个东西应该就在建树的时候进行更新
    # 然后就是在update的时候使用
    # 穿进去的还是最好的是
    def update_desc(self, items):
        self.descendants.update(items)

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


def getNode(inTree, index, ind_to_node, node_to_ind):
    """
    通过索引获取节点的名称
    inTree.children[index]的名称
    :param inTree:
    :param index:
    :param mark:
    :return:
    """
    # print("inTree is {}".format(inTree))
    # print("inTree.children is {}".format([node.name if node else None for node in inTree.children]))
    try:
        ind = node_to_ind[inTree.name]
    except KeyError:
        ind = -1
    return ind_to_node[ind + index + 1]


# 我也来写个牛逼的算法
# mark是不是应该从大到小的排列，这样好计算些？
def updateTree(items, inTree, count, mark):
    # items[0] 在inTree之中的索引位置
    # cur = mark[items[0]] - mark.get(inTree.name, 0) - 1

    # print("inTree is {}".format(inTree.name))
    # print("item is {}".format(items[0]))

    # cur算的是items[0]在inTree树的children中的索引
    # 子节点的初始化，初始化错了，傻逼
    inTree.update_desc(set(items))
    cur = getCur(items[0], inTree, mark)
    # print("index is {}".format(cur))
    # print("{}子节点的顺序为{}".format(items[0], [ele.name if isinstance(ele, TreeNode) else ele for ind, ele in enumerate(inTree.children) if ind > cur]))
    if inTree.children[cur]:
        inTree.children[cur].inc(count)
    else:
        # 初始化节点的时候，得计算孩子节点的个数
        inTree.children[cur] = TreeNode(items[0], count, [None] * (len(inTree.children) - cur - 1))
    if len(items) > 1:
        updateTree(items[1:], inTree.children[cur], count, mark)


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
            headerTable[item] = headerTable.get(item, 0) + dataSet[
                trans]
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

    retTree = TreeNode('Null Set', 1, [None] * len(apr))  # create tree
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
            updateTree(orderedItems, retTree, count, mark)  # populate tree with ordered freq itemset

    return retTree, mark


# 这个功能的使用，得提前创建一个节点，避免对原来的树造成混乱
# 影响的永远都是第一个节点
# 对第一个节点进行改造
# 还是有点问题的，并没有node完成初始化
# 好像并没有关联起来，仅仅对node1初始化为TreeNode，是不是没有用的
def mergeNode(node1, node2):
    """
    把node2节点上的数据，复制到node1上去。
    但是呢当node1位
    :param retTree:
    :param node:
    :return:
    """
    # 在节点node2不是TreeNode的时候，直接返回node1
    if not node2:
        return node1
    # 这个用来分辨，node1是节点还是字符
    # 如果是节点，直接添加值
    # 如果是字符，则需要初始化为一个节点
    if node1:
        # 这个地方相当于，仅仅对node1进行赋值，对node1的父节点的这个孩子似乎并没有任何影响
        node1.inc(node2.count)
        node1.descendants.update(node2.descendants.copy())
    else:
        # 如果维护一个headerTable的话，只需要在这更新这个headerTable了
        node1 = TreeNode(node2.name, node2.count, [None] * len(node2.children))
        node1.descendants = node2.descendants.copy()

    for ind, node in enumerate(node2.children):
        if node:
            node1.children[ind] = mergeNode(node1.children[ind], node)
    return node1


def get_node_list(inTree, index, res):
    """
    开始的时候，inTree肯定是一个节点
    所以是可以正确的走下去的
    在进行递归的调用get_node_list的时候
    就得在inTree是节点的情况下进行调用了
    :param inTree:
    :param index:
    :param res:
    :return:
    """
    # if not isinstance(inTree, TreeNode):
    #     return
    # if isinstance(inTree.children[index], TreeNode):
    if inTree.children[index]:
        res.append(inTree.children[index])
    for i in range(index - 1, -1, -1):
        if inTree.children[i]:
            get_node_list(inTree.children[i], index - i - 1, res)


def _sum(node_list):
    return reduce(lambda x, y: x + y.count, node_list, 0)


# 更新相同节点列表的节点，对其进行删除
# 删除之后呢？难道又进行寻找所有节点吗？
# 这样不是很费劲的吗
# 这个update和find是一样的套路
# 这个更新可能有点困难，感觉套路不对
def update(inTree, index):
    # print("inTree is {}".format(inTree))
    # print("index is {}".format(index))
    if inTree.children[index]:
        for ind, child in enumerate(inTree.children[index].children):
            if child:
                # 这个地方是不是也得完成赋值，因为inTree.children[ind + 1]也是可能是字符的
                # 如果是字符的话，更新上去不是也没用的吗
                # 之前的update都是有问题的啊啊啊啊！！！！！
                # 终于找到错误在哪里了，全部出现在这里
                inTree.children[ind + 1 + index] = mergeNode(inTree.children[ind + 1 + index], child)
    # 更新一个节点，就得把这个节点置为None
    """
    这个地方非常重要，如果节点设置为None之后，这个节点下的数据都不会被之后的操作访问到
    因为都是通过节点的索引，和节点得是TreeNode类型的才行
    """
    inTree.children[index] = None
    for i in range(index - 1, -1, -1):
        if inTree.children[i]:
            update(inTree.children[i], index - i - 1)


"""
时间主要就在这里
感觉改进还是有戏的
这个mineTree花费的是最多的时间
"""


def mineTree(inTree, minSup, prefix, ind_to_node, node_to_ind, res):
    """
    基本逻辑是在inTree上剔除频繁项基节点，然后再进行频繁项基的挖掘
    上面的删除是指，将将对应的节点置为None
    目前来说，两步已经合成一步了，但是呢，时间似乎并没有减少
    :param inTree:
    :param minSup:
    :param prefix:
    :param res:
    :return:
    """
    # 用来存储过滤掉的项基
    _all = set()
    # 可不可以将两遍遍历转化成一遍，这样的话是不是更快一些
    # 完成两遍遍历合成一遍遍历
    # 但是效果没有多少
    for ind, node in enumerate(inTree.children[::-1]):
        # ind一开始是逆序的
        # 经过下面的操作转化成正序的
        ind = inTree.length - ind - 1
        node_name = getNode(inTree, ind, ind_to_node, node_to_ind)
        if node_name not in inTree.descendants:
            continue
        node_list = []
        # 获取count和get_node_list能不能进行合并，这样就不必遍历两遍节点了
        get_node_list(inTree, ind, node_list)
        # print("node_list's length is {}".format(len(d[node.name if isinstance(node, TreeNode) else node])))
        count = reduce(lambda x, y: x + (y.count if y else 0), node_list, 0)

        # print("node's count is {}".format(count))
        if count < minSup:
            # _all.add(node.name if isinstance(node, TreeNode) else node)
            update(inTree, ind)
            # inTree.descendants.remove(node_name)
            _all.add(node_name)
        else:
            # print("new item_sets is {}".format(prefix + [node_name]))
            res.append(prefix + [node_name])
            node = TreeNode(node_name, 0, [None] * len(node_list[0].children))
            # 可不可以在mergeNode的过程中，返回一个headerTable来
            reduce(mergeNode, node_list, node)
            node.descendants -= _all
            mineTree(node, minSup, prefix + [node.name], ind_to_node, node_to_ind, res)
    """
    第一步和第二步，可以是分离的吧？
    如果第一步清理为None的节点，对第二步是不会造成影响的
    """

    # 第二遍的时候，添加到结果之中
    # for ind, node in enumerate(inTree.children):
    #     # node_name = getNode(inTree, ind, ind_to_node, node_to_ind)
    #     # if not node_name in inTree.descendants: continue
    #     node_name = node.name if node else getNode(inTree, ind, ind_to_node, node_to_ind)
    #     # if node:
    #     #     print("node.name == getNode {}".format(getNode(inTree, ind, ind_to_node, node_to_ind) == node.name))
    #     if node_name not in inTree.descendants:
    #         continue
    #     print("new item_sets is {}".format(prefix + [node_name]))
    #     res.append(prefix + [node_name])
    #     # node_list = []
    #     # get_node_list(inTree, ind, node_list)
    #     node_list = d[node_name]
    #     # 这个为什么会出现list index out of range的错误
    #     node = TreeNode(node_name, 0, [None] * len(node_list[0].children))
    #     reduce(mergeNode, node_list, node)
    #     node.descendants -= _all
    #     mineTree(node, minSup, prefix + [node.name], ind_to_node, node_to_ind, res)


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
    retTree, node_to_ind = createTree(retDict, minSup)
    ind_to_node = {value: key for key, value in node_to_ind.items()}
    retTree.disp()
    res = []
    mineTree(retTree, minSup, [], ind_to_node, node_to_ind, res)
    print("length is {}".format(len(res)))
    # for line in res:
    #     print(line)
    print("cost time is {}".format(time.time() - start))


def test_function():
    start = time.time()
    # dataset = [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]
    # dataset = [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5']]
    dataset = [['bread', 'milk', 'vegetable', 'fruit', 'eggs'],
               ['noodle', 'beef', 'pork', 'water', 'socks', 'gloves', 'shoes', 'rice'],
               ['socks', 'gloves'],
               ['bread', 'milk', 'shoes', 'socks', 'eggs'],
               ['socks', 'shoes', 'sweater', 'cap', 'milk', 'vegetable', 'gloves'],
               ['eggs', 'bread', 'milk', 'fish', 'crab', 'shrimp', 'rice']]
    # dataset = [[1,2,5],[2,4],[2,3],[1,2,4],[1,3],[2,3],[1,3],[1,2,3,5],[1,2,3]]
    minSup = 3
    retDict = createInitSet(dataset)
    # for key, value in retDict.items():
    #     print("{} => {}".format(key, value))
    retTree, node_to_ind = createTree(retDict, minSup)
    retTree.disp()
    ind_to_node = {value: key for key, value in node_to_ind.items()}

    result = []
    mineTree(retTree, minSup, [], ind_to_node, node_to_ind, result)
    print("length is {}".format(len(result)))
    for res in result:
        print(res)

    print("cost is {}".format(time.time() - start))


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
