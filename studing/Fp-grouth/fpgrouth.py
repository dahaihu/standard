"""
如何在一棵树上，挖掘频繁一项集，二项集，三项集等等
条件模式基：是以所查找元素项为结尾的路径集合，表示的是所查找的元素项与树根节点之间的所有内容。
"""

class treeNode:
    # 名字，次数，父节点
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue  # 当前节点的名称
        self.count = numOccur  # 当前节点在此模式下的出现次数
        self.nodeLink = None  # 用来指向跟当前节点name相同的，别的支上的节点
        self.parent = parentNode  # needs to be updated    #用来指向当前节点，在此支上的父节点
        self.children = {}  # 当前节点的孩子节点

    def inc(self, numOccur):  # 由于事务是含有次数的，所以，当前节点出现的频次可能是多余1的，所以加上numOccur
        self.count += numOccur

    def disp(self, ind=1):  # 这个应该是通过“作图”(就是打印)来描述数，那么这个是如何打印的呢？拥有一个父节点的孩子，在同一层
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)


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
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]  # 这个dataSet[trans] 有点让人摸不着头脑   传入的dataset是不是经过处理的。

    # 字典不能边遍历，边删除吗？对的，字典是不能遍历的同事进行删除的

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
    # 对headerTable中的头结点进行排序
    # 键为节点，值为节点出现的频次从大到小排序的索引
    # 也就是说索引越小值越大
    mark = {node:ind for ind, node in enumerate(sorted(headerTable, key=lambda x:headerTable[x], reverse=True))}

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
    retTree = treeNode('Null Set', 1, None)  # create tree
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
            if item in mark:
                localD[item] = mark[item]
        # localD用来存放该事务记录中，每个频繁项的频次
        if len(localD) > 0:
            # 对频繁项按照出现的次数进行从大到小的排序
            """
            这个地方是有问题的，觉得相同的数量的项，在不同的组合中，顺序可能是不一致的
            最好前面统一制定排序
            """
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1])]
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

        inTree.children[items[0]] = treeNode(items[0], count, inTree)

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


def updateHeader(nodeToTest, targetNode):  # this version does not use recursion
    while (nodeToTest.nodeLink != None):  # Do not use recursion to traverse a linked list! 为什么不要通过递归遍历一个链表
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# 找节点的前缀，把当前节点包含在prefixPath之中的，这个后面会有提醒，需要注意的
# 这个和下面的findPrefixPath是什么关系呢？
def ascendTree(leafNode, prefixPath):  # ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


# 这个是用来干什么的呢？这个basePat是用来干什么的？我怎么没看见函数里面用着这个参数
# 返回的结果是以treeNode为尾的所有频繁项集
# 但是这个basePat到底是干嘛的呢？
# 既然命名为findPrefixPath，那么就只需要一个参数
# 这样的话，不就跟ascendTree功能是一样的
# 不是的，比ascendTree多些功能
# 找寻该条件的所有条件模式基
# 这个treeNode是一个链表，一直往下指向一个nodeName相同的节点

# 返回一个节点之上的模式？
#     a5
#    b3 c4
#    c2
# 如果传入C节点，那么返回的就是{frozenset(a,b):2,frozenset(a):4}
# 这个传入的basePat是干嘛用的呢？
"""
这个傻逼的basePat是用来干嘛的
这个函数是用来找条件模式基的
然后基于这些条件模式基来构建一个新的树
找到输入的treeNode的条件模式基。。。。

这个里面传入的basePat有个jbd用
"""
def findPrefixPath(basePat, treeNode):  # treeNode comes from header table 、treeNode是来自headerTable的
    condPats = {}
    # treeNode = headTable[basePat][1]
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            # 为什么把找到的prefixPath之中第一个排除在外
            # 因为通过ascendTree找寻prefixPath的时候，把当前的treeNode也包含在其中了
            # 在一个字典中，可变对象是不能作为键的。出错的原因是not hashble
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


# 如何在一棵树中，寻找频繁项集呢？
# 在树种挖掘频繁项集吗？？？？？
# 这个headerTable之前就存在吗？
# 这个inTree和这个headerTable是相对应的
# 这个preFix我觉得叫后缀更好
"""
代码似乎要写的好，写的精简，只能用递归
而自己写递归的话，要注意的地方很多，截止条件，，，，，
这个也是个递归
"""
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    # 这个bigL是根据按照频繁项的频率从小到大排序的频繁项
    # 这个bigL是从headerTable中来的
    # 这个bigL的顺序，影响结果吗?
    # print("headerTable is {}".format(headerTable))
    # print("preFix is {}".format(preFix))
    # 每mineTree一次都得对headerTable中的键按照频次从小到大排序一次的吗？
    # 而且，这个headerTable也是不变得的吧？？？？？
    # 这个地方sort一下有用吗？
    # 从底部网上走，和乱序的走，有什么区别的吗
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0], reverse=True)]  # (sort header table)
    # print("bigL is {}".format(bigL))
    # 这个basePat是单个项
    for basePat in bigL:  # start from bottom of header table
        # newFreqSet = preFix.copy()
        # newFreqSet.add(basePat)  # 把当前的basePat加到这个newFreqSet中去
        newFreqSet = preFix + [basePat]
        # 但是呢，这个newFreqSet就是频繁项集吗？？？？？？？
        # print 'finalFrequent Item: ',newFreqSet    #append to set
        print("newFreqSet is {}".format(newFreqSet))
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        # print 'condPattBases :',basePat, condPattBases
        # 2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead = createTree(condPattBases, minSup)
        # print 'head from conditional tree: ', myHead
        if myHead != None:  # 3. mine cond. FP-tree
            # print 'conditional tree for: ',newFreqSet
            # myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


# 这个createIniSet是不是有点不好。假如有的有多个相同的事务，那么该事物数是不是可以是大于1的，如果都是1，那么这么做有什么意义呢？
# 看了上面这条评论，我是搞懂了，我之前是怎么的笨
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0) + 1
    return retDict


# dataSet=createInitSet(loadSimpDat())
# print(dataSet)

def loadDataset(path, minSup):
    dataset = []
    with open(path, 'r') as file:
        count = 0
        for line in file:
            # print(line.strip().split(' '))
            dataset.append(line.strip().split(' '))
            count += 1
    minSup = len(dataset) * minSup
    return dataset, minSup

from time import time
def fp_test(path, minSup):
    start = time()
    simpDat, minSup = loadDataset(path, minSup)
    # minSup = 2
    # simpDat = [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]
    # simpDat = [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5']]


    initSet = createInitSet(simpDat)
    print('数据集的长度为 {}'.format(len(initSet)))
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    myFPtree.disp()
    myFreqList = []
    print('minSup is {}'.format(minSup))
    mineTree(myFPtree, myHeaderTab, minSup, [], myFreqList)
    print("myFreqList is {}".format(len(myFreqList)))
    # for items in myFreqList:
    #     print(items)
    print('cost time is {}'.format(time() - start))

fp_test(r'/Users/hushichang/mushroom.dat.txt', 0.2)