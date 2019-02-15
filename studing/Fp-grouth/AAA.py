"""
a better solution?????

fpgrouth树的事务记录添加的时候，似乎对事务记录并没有进行排序

这个算法会比Fp-grouth算法更快的吗？？？？？？？？？

"""
from functools import reduce


class TreeNode:
    # 名字，次数，父节点
    def __init__(self, nameValue, numOccur):
        self.name = nameValue  # 当前节点的名称
        self.count = numOccur  # 当前节点在此模式下的出现次数
        self.nodeLink = None  # 用来指向跟当前节点name相同的，别的支上的节点
        self.children = {}  # 当前节点的孩子节点

    def inc(self, numOccur):  # 由于事务是含有次数的，所以，当前节点出现的频次可能是多余1的，所以加上numOccur
        self.count += numOccur

    def disp(self, ind=1):  # 这个应该是通过“作图”(就是打印)来描述数，那么这个是如何打印的呢？拥有一个父节点的孩子，在同一层
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

    def __str__(self):
        return 'node is {}, node.count is {}, node.children is {}'.format(self.name, self.count,
                                                                          [node for node in self.children])


# 更新节点
def updateHeader(node, targetNode):
    while node.nodeLink != None:
        node = node.nodeLink
    node.nodeLink = targetNode


# 合并两个树
# 都往第一个节点上合并
# node1和node2的节点的元素值是相同的
def mergeNode(node1, node2):
    node1.inc(node2.count)
    intersect = node1.children.keys() & node2.children.keys()
    for node in intersect:
        node1.children[node].inc(node2.children[node].count)
        mergeNode(node1.children[node], node2.children[node])
    for node in (node2.children.keys() - node1.children.keys()):
        node1.children[node] = node2.children[node]
    return node1

def createHeaderTable(node):
    headerTable = {}
    pass

def updateTree(node, headerTable, minSup):
    pass

def test_mergeNode():
    a1 = TreeNode('a', 1)
    b1 = TreeNode('b', 2)
    c1 = TreeNode("c", 1)
    c2 = TreeNode("c", 1)
    d1 = TreeNode('d', 1)

    a1.children['b'] = b1
    a1.children['c'] = c1
    b1.children['c'] = c2
    b1.children['d'] = d1

    a1.disp()

    a2 = TreeNode("a", 1)
    b2 = TreeNode("b", 2)
    d2 = TreeNode("d", 1)
    d3 = TreeNode("d", 1)
    e = TreeNode('e', 1)

    a2.children['b'] = b2
    a2.children['d'] = d3
    b2.children['d'] = d2
    b2.children['e'] = e

    a2.disp()

    aaa = mergeNode(a1, a2)

    aaa.disp()


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
                trans]  # 这个dataSet[trans] 有点让人摸不着头脑   传入的dataset是不是经过处理的。

    # 字典不能边遍历，边删除吗？对的，字典是不能遍历的同时进行删除的

    # for k in headerTable.keys():  #remove items not meeting minSup #我觉得出现错误的原因是，headerTable是中的值是可变的，这个headerTable.keys()
    #     if headerTable[k] < minSup:
    #         del(headerTable[k])

    # 这个用filter会失败的，filter似乎只能滤除列表？？？？？反正是不能用来滤除字典的(如果把字典当成iterable对象来看的话，里面返回的是全部键)
    # filter可以滤除任何iterable对象
    # headerTable=filter(lambda x:headerTable[x]>=minSup,headerTable)
    # 将出现频次小于最低支持度的频繁项给删除
    s = set(headerTable.keys())
    for ind in s:
        if headerTable[ind] < minSup:
            del headerTable[ind]

    # 现在的这个headerTable中的键是频繁项，值是频繁项出现的次数
    freqItemSet = set(headerTable.keys())  # 频繁项集，这个不用set函数处理，是不是也是可以的。？？？  freqItemSet=set(headerTable)即可
    # print 'freqItemSet: ',freqItemSet
    if len(freqItemSet) == 0: return None, None  # if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # reformat headerTable to use Node link
    # 现在这个headerTable变成了，键依然是频繁项，但是值变成了，一个含有两个对象的列表，第一个对象是原来的值，即频繁项出现的次数；第二个对象是None
    # print 'headerTable: ',headerTable
    # treeNode的三个参数，名字，数量，父节点
    # 现在开始建树了
    retTree = TreeNode('Null Set', 1)  # create tree
    # 第二遍过滤数据库，建树
    for tranSet, count in dataSet.items():  # go through dataset 2nd time 一猜就知道dataSet是经过处理的数据集合
        # tranSet是指事务，count是指当前事务的频次
        # 对每个事务进行处理，然后添加到树中去
        # localD是用来对当前事务进行处理
        # 统计当前事务中每个频繁项出现的频次
        # 对超过最小支持度的频繁项，通过从大到小的排序方式
        # 整理成orderedItems
        localD = {}  # 这个是用来干什么的？？？用来获取当前事务中所含的频繁项集
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        # localD用来存放该事务记录中，每个频繁项的频次
        if len(localD) > 0:
            # 对频繁项按照出现的次数进行从大到小的排序
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            print("orderedItems is {}".format(orderedItems))
            ##总的应该是，对每个事物的项目，根据项目的频率，按照从大到小的排序
            updateTree(orderedItems, retTree, headerTable, count)  # populate tree with ordered freq itemset
    return retTree, headerTable  # return tree and header table


# 项目列表，项目列表应该在的根节点，表头，项目对应的数量
# items应该是频繁项中已经包含的项集
# 这个headerTable是inTree的对应
# 那么这个count指的是什么呢?
# 当前节点出现的频次
# 这个updateTree还是个递归，牛逼？？？
# 每个inTree都是一棵树，有孩子节点，有父节点，有出现的频次
def updateTree(items, inTree, headerTable, count):
    # 如果items[0]在当前节点的孩子之中的话
    if items[0] in inTree.children:  # check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count)  # increment count
    # 如果items[0]不在当前节点的孩子当中
    else:  # add items[0] to inTree.children
        inTree.children[items[0]] = TreeNode(items[0], count)

        # 如果添加到当前树的节点，没有headerTable中的链接，则添加到其中
        if headerTable[items[0]][1] is None:  # update header table
            headerTable[items[0]][1] = inTree.children[items[0]]
        # 如果有的话，则需要更新headTable，那么是如何更新这个headerTable的呢？
        # 一个个便利，直到找到最后一个，然后进行连接
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    # 由于item[0]已经添加到树中，如果item的长度等于1，那么不需要往下添加了
    if len(items) > 1:  # call updateTree() with remaining ordered items
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)


# 这个createIniSet是不是有点不好。假如有的有多个相同的事务，那么该事物数是不是可以是大于1的，如果都是1，那么这么做有什么意义呢？
# 看了上面这条评论，我是搞懂了，我之前是怎么的笨
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0) + 1
    return retDict


def depthNode(node, minSup, res, pre):
    """
    node表示当前要挖掘的节点
    minSup表示支持度
    res表示保存频繁项基的结果
    pre表示node节点的前缀
    :param node:
    :param minSup:
    :param res:
    :param pre:
    :return:
    """
    # 这个总是深度优先的吧？
    # 进行深度优先
    print("node is {}".format(node))
    if node.count >= minSup:
        res.append([node.name] + pre)
        for child in node.children.values():
            depthNode(child, minSup, res, pre + [node.name])


def mineTree(headerTable, minSup):
    res = []
    for node in headerTable:
        tmp = []
        link = headerTable[node][1]
        while link:
            tmp.append(link)
            link = link.nodeLink
        node = reduce(mergeNode, tmp)
        node.disp()
        depthNode(node, minSup, res, [])
    return res


dataset = [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5'], ['2', '3', '1']]
dataset = createInitSet(dataset)
retTree, headerTable = createTree(dataset, minSup=2)
# for key, value in headerTable.items():
#     print("{} => {}".format(key, value))
# a = headerTable['1'][1]
# count = 0
# while a:
#     count += 1
#     a = a.nodeLink
# print("count is {}".format(count))
retTree.disp()
aaa = mineTree(headerTable, 2)
for ele in aaa:
    print(ele)

# retTree.disp()
