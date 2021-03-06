import time
from functools import reduce

"""
代码里很多用数组的索引当做键来进行操作的，这个很有意思
"""


class SortedTree:
    def __init__(self, node, prefix, result, min_sup, dataset=None):
        """

        :param node: 该节点的值
        :param prefix: 包含该节点的前缀
        :param result: 用来保存结果的
        :param min_sup: 最小支持度
        :param dataset: 该节点包含的数据集
        """
        self.result = result
        self.node = node
        # 这个节点的prefix是包括当前节点的
        self.prefix = prefix
        self.support = 0
        self.min_sup = min_sup
        self.children = []
        self.dataset = [] if not dataset else dataset

    def canLinked(self):
        return len(self.dataset) >= self.min_sup

    # 给一个节点添加前缀，那么就是该节点的前缀，加上该节点的值
    def addChild(self, node):
        # print("mark is {}".format(mark))
        self.children.append(SortedTree(node, self.prefix | (1 << node), self.result, self.min_sup))

    # 给该节点添加包含该节点前缀的事务
    def addTransaction(self, transaction):
        self.dataset.append(transaction)

    # 获取该节点在排序频繁一项集中的位置
    def index(self, mark):
        return mark[self.node]

    # 对该节点进行剪枝
    def valid_candidate(self, candidate, fpset):
        right = 0
        left = candidate
        while left:
            tmp = left & (left - 1)
            cur = tmp ^ left
            if (tmp | right) not in fpset:
                return False
            right |= cur
            left = tmp
        return True


    # 这一部分的计算通过广度优先的策略
    def linking_width_first(self, fqsets, pre=True):
        if pre:
            self.children = [child for child in self.children if self.valid_candidate(child.prefix, fqsets)]
        tmp = [(1 << child.node) for child in self.children]
        # print("tmp is {}".format(tmp))
        """
        能不能在给对孩子节点进行筛选呢？
        第一步，给每个孩子节点分数据
        """
        # 划分数据集
        # print("dataset's length is {}".format(len(self.dataset)))
        for transaction in self.dataset:
            for ind, ttt in enumerate(tmp):
                if transaction & ttt == ttt:
                    self.children[ind].addTransaction(transaction)
                    # break

        """
        第二步，筛选不是频繁项集的子节点

        这个不就是相当于已经过滤了一遍了吗？
        那你个煞笔的第三步是用来干什么的？
        用来浪费时间的吗？
        傻屌东西

        这样的话，速度可以提升多少呢？

        可以一倍的吗？

        """
        self.children = [child for child in self.children if len(child.dataset) >= self.min_sup]
        # cur = 0
        # while cur < len(self.children):
        #     if len(self.children[cur].dataset) < self.min_sup:
        #         del self.children[cur]
        #     else:
        #         cur += 1
        """
        第三步，给孩子节点分可能的子节点
        感觉在这个地方筛选子节点也是没有问题的啊！
        这个不就是相当于
        """
        for i in range(len(self.children) - 1):
            for j in range(i + 1, len(self.children)):
                self.children[i].addChild(self.children[j].node)
                # # 这一部分注释，是可以在这进行候选项集的剪枝操作
                # if pre or self.valid_candidate([self.children[j].node] + self.children[i].prefix, fqsets):
                #     self.children[i].addChild(self.children[j].node)

        self.support = len(self.dataset)
        del self.dataset
        # """
        # 第三步，对孩子节点进行深度优先的挖掘
        # 这一步是不是应该在外部做，这样可以按照广度优先的方式来计算，从而过滤掉没必要的项集
        # """
        # for child in self.children:
        #     if child.canLinked():
        #         self.result.append([child.node] + self.prefix)
        #         child.linking_width_first(mark)


class Best:
    """
    dataset: 原始的数据集
    mark: 单项集 和 支持度， 以后的每个事务记录的排序都是根据这个进行排序
    """

    def __init__(self, minSup, dataset=None):
        self.dataset = dataset if dataset else self.loadDataSet()
        self.minSup = minSup
        self.mark = {}
        self.res = None

    def loadDataSet(self):
        return [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5']]
        # return [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]

    def scanDataset(self):
        for items in self.dataset:
            for item in items:
                self.mark[item] = self.mark.get(item, 0) + 1
        for key, count in self.mark.items():
            print("{} => {}".format(key, count))
        self.mark = {key: value for key, value in self.mark.items() if value >= self.minSup}
        # 对键(键是频繁一项集，值是对应的支持度)从大到小排列
        self.res = sorted(self.mark, key=lambda x: self.mark[x], reverse=True)
        self.fk_1 = self.mark
        print("fk_1 is {}".format(self.fk_1))
        # 这个mark是用来是的每个节点进行移动然后找到对应的位置的
        self.mark = {node: (len(self.res) - ind - 1) for ind, node in enumerate(self.res)}

    # 这个地方fk1，看情况应该是从大到小排序就可以正确的编码了
    # 因为值是从小到大进行排列
    # 从后又从前到后的判断
    # 前面的移动的位次是最多的
    # 这个fk1，传入的是self.res
    def encode(self, fk1, data):
        print("data is {}".format(data))
        print("fk1 is {}".format(fk1))
        encodedAffair = []
        # 传入的数据集里面，事务记录是用set来进行存储的是不是更快一些？
        # 但是这部分本来就够快的
        for a in data:
            tmp = 0
            for ele in fk1:
                tmp = (tmp << 1) + 1 if ele in a else tmp << 1
            # 实际上的运算还是得用这个
            encodedAffair.append(tmp)
            # 这个可以用来做视觉上的展示
            # res.append(bin(tmp))
        return encodedAffair

    def encode_transaction(self, fk1, data):
        tmp = 0
        for ele in fk1:
            tmp = (tmp << 1) + 1 if ele in data else tmp << 1
        return tmp

    def main(self):
        result = []
        self.scanDataset()
        # print("fk_1 is {}".format(self.fk_1))
        # encode传入的应该是按照频繁项集从小到大排序的数组
        data = self.encode(self.res, self.dataset)
        for line in data:
            print(bin(line))
        # # 展示编码结果
        # return data
        root = SortedTree('', 0, result, self.minSup, data)
        # print("self.res is {}".format(self.res))
        print("self.mark is {}".format(self.mark))
        length = len(self.res)
        for i in range(length):
            root.addChild(length - 1 - i)
        res = [root]
        count = 0
        while res:
            count += 1
            print("频繁{}项集的个数为{}".format(count - 1, len(res)))
            print("cost time is {}".format(time.time() - start))
            tmp = []
            result.append(set())
            for node in res:
                if not node.children:
                    continue
                if count > 2:
                    node.linking_width_first(result[-2], pre=True)
                else:
                    node.linking_width_first(set(), pre=False)
                for child in node.children:
                    tmp.append(child)
                    result[-1].add(child.prefix)

            res = tmp
        print("result is {}".format(reduce(lambda x, y: x + len(y), result, 0)))

        for FK in result:
            print(FK)
        print(len(result))


def loadDataset(path):
    dataset = []
    with open(path, 'r') as file:
        for line in file:
            print(line.strip().split(' '))
            dataset.append(line.strip().split(' '))
    minSup = len(dataset) * 0.2
    return minSup, dataset


if __name__ == '__main__':
    # loadDataset(r'C:\Users\shichang.hu\Desktop\mushroom.dat.txt')
    start = time.time()
    # minSup, dataset = loadDataset(r'C:\Users\shichang.hu\Desktop\mushroom.dat.txt')
    # dataset = [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]
    # dataset = [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5'], ['2', '3', '1']]
    # dataset = [['bread', 'milk', 'vegetable', 'fruit', 'eggs'],
    #            ['noodle', 'beef', 'pork', 'water', 'socks', 'gloves', 'shoes', 'rice'],
    #            ['socks', 'gloves'],
    #            ['bread', 'milk', 'shoes', 'socks', 'eggs'],
    #            ['socks', 'shoes', 'sweater', 'cap', 'milk', 'vegetable', 'gloves'],
    #            ['eggs', 'bread', 'milk', 'fish', 'crab', 'shrimp', 'rice']]
    # dataset = [[1,2,5],[2,4],[2,3],[1,2,4],[1,3],[2,3],[1,3],[1,2,3,5],[1,2,3]]
    # minSup = 2
    minSup, dataset = loadDataset(r'/Users/hushichang/mushroom.dat.txt')
    # b = Best(2, dataset)
    b = Best(minSup, dataset)
    # b = Best(0.2, dataset=loadDataset(r'/Users/hushichang/mushroom.dat.txt'))
    # b = Best(2)
    # b = Best(0.2)
    res = b.main()
    # for ele in res:
    #     print(ele)
    print('cost time is {}'.format(time.time() - start))
