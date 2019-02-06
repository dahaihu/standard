from functools import reduce

"""
全部都不需要headerTable
根据孩子节点的索引来进行计算

如何初始化这棵树呢？

如何递归的合并节点呢？

children 存储的是字符， 或者该字符对应的TreeNode

"""


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

    def __str__(self):
        return 'node is {}, node.count is {}, node.children is {}'.format(self.name, self.count,
                                                                          [node for node in self.children])


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0) + 1
    return retDict


def getCur(node, inTree, mark):
    """
    :param node: 节点的名字
    :param inTree: 父节点
    :param mark: 通过mark获取节点的位置
    :return:
    """
    # mark没有获取到inTree.name的时候，说明是根节点
    # 然后
    return mark[node] - mark.get(inTree.name, -1) - 1


# 我也来写个牛逼的算法
# mark是不是应该从大到小的排列，这样好计算些？
def updateTree(items, inTree, count, mark, apr):
    # items[0] 在inTree之中的索引位置
    # cur = mark[items[0]] - mark.get(inTree.name, 0) - 1

    # print("inTree is {}".format(inTree.name))
    # print("item is {}".format(items[0]))

    # cur算的是items[0]在inTree树的children中的索引
    # 子节点的初始化，初始化错了，傻逼
    cur = getCur(items[0], inTree, mark)
    # print("index is {}".format(cur))
    # print("{}子节点的顺序为{}".format(items[0], [ele.name if isinstance(ele, TreeNode) else ele for ind, ele in enumerate(inTree.children) if ind > cur]))
    if isinstance(inTree.children[cur], TreeNode):
        inTree.children[cur].inc(count)
    else:
        # 初始化节点的时候，得计算孩子节点的个数
        inTree.children[cur] = TreeNode(items[0], count, [ele.name if isinstance(ele, TreeNode) else ele for ind, ele in enumerate(inTree.children) if ind > cur])
    if len(items) > 1:
        updateTree(items[1:], inTree.children[cur], count, mark, apr)


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

    retTree = TreeNode('Null Set', 1, apr.copy())  # create tree
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
            updateTree(orderedItems, retTree, count, mark, apr)  # populate tree with ordered freq itemset

    return retTree


# 这个功能的使用，得提前创建一个节点，避免对原来的树造成混乱
# 影响的永远都是第一个节点
# 对第一个节点进行改造
# 还是有点问题的，并没有node完成初始化
# 好像并没有关联起来，仅仅对node1初始化为TreeNode，是不是没有用的，
def mergeNode(node1, node2):
    """
    功能还是分开的写比较好
    :param retTree:
    :param node:
    :return:
    """
    # 在节点node2不是TreeNode的时候，直接返回node1
    if not isinstance(node2, TreeNode):
        return node1
    # 这个用来分辨，node1是节点还是字符
    # 如果是节点，直接添加值
    # 如果是字符，则需要初始化为一个节点
    if not isinstance(node1, TreeNode):
        # 这个地方相当于，仅仅对node1进行赋值，对node1的父节点的这个孩子似乎并没有任何影响
        node1 = TreeNode(node1, node2.count, [node.name if isinstance(node, TreeNode) else node for node in node2.children])
    else:
        node1.inc(node2.count)

    # 由于是往node1上添加字符或者什么的
    # 所以只需要管理node2上的children
    # 需要进行递归的操作
    for ind, node in enumerate(node2.children):
        if isinstance(node, TreeNode):
            node1.children[ind] = mergeNode(node1.children[ind], node)
    return node1

def get_node_list(inTree, index, res):
    if (not inTree) or isinstance(inTree, str):
        return
    if isinstance(inTree.children[index], TreeNode):
        res.append(inTree.children[index])
    for i in range(index - 1, -1, -1):
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
    if isinstance(inTree.children[index], TreeNode):
        for ind, child in enumerate(inTree.children[index].children):
            if isinstance(child, TreeNode):
                # 这个地方是不是也得完成赋值，因为inTree.children[ind + 1]也是可能是字符的
                # 如果是字符的话，更新上去不是也没用的吗
                # 之前的update都是有问题的啊啊啊啊！！！！！
                # 终于找到错误在哪里了，全部出现在这里
                inTree.children[ind + 1 + index] = mergeNode(inTree.children[ind + 1 + index], child)
    # 更新一个节点，就得把这个节点置为None
    inTree.children[index] = None
    for i in range(index - 1, -1, -1):
        if isinstance(inTree.children[i], TreeNode):
            update(inTree.children[i], index - i - 1)



"""
时间主要就在这里
感觉改进还是有戏的
"""
def mineTree(inTree, minSup, prefix, res):
    """
    基本逻辑是在inTree上剔除频繁项基节点，然后再进行频繁项基的挖掘
    :param inTree:
    :param minSup:
    :param prefix:
    :param res:
    :return:
    """
    # _all = {node.name for node in inTree.children if node}
    # print("res is {}".format(res))
    # inTree.disp()
    # _all = set()
    # 第一遍过滤的时候，统计支持度，然后更新树
    ll = len(inTree.children)
    for ind, node in enumerate(inTree.children[::-1]):
        if not node: continue
        # 之前逆序更新树的时候，index都是计算错的
        ind = ll - ind - 1
        node_list = []
        """
        照理说get_node_list没问题的话，update也不会有问题的
        压根并没有对节点的children的长度进行修改，为什么会在inTree.children[index]上出现list index out of range的exception呢？
        """
        get_node_list(inTree, ind, node_list)
        count = reduce(lambda x, y: x + (y.count if isinstance(y, TreeNode) else 0), node_list, 0)
        if count < minSup:
            # _all.add(node.name if isinstance(node, TreeNode) else node)
            update(inTree, ind)
    """
    第一步和第二步，可以是分离的吧？
    如果第一步清理为None的节点，对第二步是不会造成影响的
    """

    # 第二遍的时候，添加到结果之中
    for ind, node in enumerate(inTree.children):
        if not node: continue
        res.append(prefix + [node.name if isinstance(node, TreeNode) else node])
        node_list = []
        get_node_list(inTree, ind, node_list)
        if node_list:
            # 每次挖掘的树，都是新创建的
            node = TreeNode(node.name if isinstance(node, TreeNode) else node, 0, [child.name if isinstance(child, TreeNode) else child for child in node_list[0].children])
            reduce(mergeNode, node_list, node)
            mineTree(node, minSup, prefix + [node.name], res)


def loadDataset(path, _max=float('inf')):
    dataset = []
    with open(path, 'r') as file:
        count = 0
        for line in file:
            count += 1
            print(line.strip().split(' '))
            dataset.append(line.strip().split(' '))
            if count >= _max:
                break
    minSup = len(dataset) * 0.3
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
    retTree = createTree(retDict, minSup)
    retTree.disp()

    res = []
    mineTree(retTree, minSup, [], res)
    for line in res:
        print(line)
    print("cost time is {}".format(time.time() - start))

def test_function():
    # dataset = [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]
    dataset = [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5']]
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
    result = []
    mineTree(retTree, minSup, [], result)
    print("length is {}".format(len(result)))
    for res in result:
        print(res)


def test_update():
    # dataset = [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]
    dataset = [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5']]
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
    # final_test()
    test_function()
    # test_update()

