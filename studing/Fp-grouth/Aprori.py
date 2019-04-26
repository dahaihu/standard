import time


class BE_Apriori:
    def __init__(self, affair, minSup):
        self.minSup = minSup * len(affair)
        self.affair = affair
        self.result = []
        # 获取频繁1-项集,,,这个fk1，只在初始化的时候使用，所以，不用设置为实例的属性
        fk1 = self.get_fk1()
        print('fk1=>', fk1)
        # print("事务原始记录为", self.affair)

        self.encodedAffair = self.encode(fk1, self.affair)
        # print('编码后的事务', self.encodedAffair)
        encoded_fk1 = self.encode(fk1, [set((ele,)) for ele in fk1])
        print("编码后的频繁1-项集", encoded_fk1)
        self.result.append(encoded_fk1)
        # 对事务进行编码

        # 获取候选2-项集
        cfk2 = self.apriori_gen_1(encoded_fk1)
        # print('候选二项集',cfk2)
        # 获取频繁2-项集
        self.fk2 = self.get_fk(cfk2)
        print('fk2', self.fk2)
        self.result.append(self.fk2)
        # self.fk2=set(self.fk2)

    # 计算候选项集的支持度，并对低于支持度的数据进行剔除
    def get_fk(self, cfk):
        res = set()
        for ele in cfk:
            count = 0
            for a in self.encodedAffair:
                if a & ele == ele:
                    count += 1
            if count >= self.minSup:
                res.add(ele)
        return list(res)

    # 通过频繁1-项集，产生候选频繁2-项集
    # 这个频繁1-项集应该是编码后的结果
    def apriori_gen_1(self, f1):
        num = len(f1)
        res = set()
        for i in range(num - 1):
            for j in range(i + 1, num):
                res.add(f1[i] + f1[j])
        return res

    # 通过频繁k项集，获取候选频繁(k+1)-项集
    def apriori_gen_2(self, fk, fk2):
        num = len(fk)
        res = set()
        for i in range(num - 1):
            for j in range(i + 1, num):
                if fk[i] ^ fk[j] in fk2:
                    res.add((fk[i] ^ fk[j]) + (fk[i] & fk[j]))
        return res

    # 获取频繁1-项集
    # 返回的频繁1-项集由单个项来表示
    # 这个好像是并没有排序的啊
    def get_fk1(self):
        res = {}
        for a in self.affair:
            for ele in a:
                res[ele] = res.get(ele, 0) + 1
        # print(res)
        return [k for k, v in res.items() if v >= self.minSup]

    # 根据频繁1-项集对事务进行编码
    # 返回的结果为二进制数,实际上为十进制数
    # 这个事务是指事务集
    # @staticmethod 测试的时候用的
    def encode(self, fk1, data):
        encodedAffair = []
        for a in data:
            tmp = 0
            for ele in fk1:
                # print('ele:',ele)
                # print('a:',a)
                tmp = (tmp << 1) + 1 if ele in a else tmp << 1
            # 实际上的运算还是得用这个
            encodedAffair.append(tmp)
            # 这个可以用来做视觉上的展示
            # res.append(bin(tmp))
        return encodedAffair

    def main(self):
        cfk = self.apriori_gen_2(self.fk2, self.fk2)
        self.fk2 = set(self.fk2)
        k = 3
        while cfk:
            fk = self.get_fk(cfk)
            print('fk%d=>' % k, fk)
            self.result.append(fk)
            cfk = self.apriori_gen_2(fk, self.fk2)
            k += 1
        return self.result


class AprioriP:
    def __init__(self, dataSet, minsup):
        self.dataSet = dataSet
        self.minsup = minsup

    def loadDataSet(self):
        # return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
        return [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]

    # 找出所有的单个项 返回的是列表
    def createC(self, dataset):
        C = []
        for data in dataset:
            for a in data:
                if not [a] in C:
                    C.append([a])
        return list(map(frozenset, C))

    # 扫描数据库，获取所有的频繁项集，和其支持度，这个里面的支持度是百分比计算的
    # 需要注意的是D和Ck里面的元素都是集合
    # D是列表  Ck是集合  它们之中的元素，全是frozenset
    # 注意判断一个项集是否是另一个项集的子集，需要用到集合中的issubset方法
    # 返回的是集合包围的频繁项集，和字典，其键为频繁项集，其值为支持度
    def scanD(self, D, Ck, minSupport):
        ssCnt = {}
        for tid in D:
            for can in Ck:
                if can.issubset(tid):
                    if not can in ssCnt:
                        ssCnt[can] = 1
                    else:
                        ssCnt[can] += 1
        numItems = float(len(list(D)))
        retList = set()
        supportData = {}
        for key in ssCnt:
            support = ssCnt[key] / numItems
            if support >= minSupport:
                retList.add(key)
                supportData[key] = support
        return retList, supportData

    # 返回的候选项集以集合的方式返回，可以减少候选项集的产生，避免了对于同样的项集，要多次遍历数据库
    def aprioriGen(self, Lk, k):
        # print(Lk)
        retList = set()
        lenLk = len(Lk)
        Lk = list(Lk)
        for i in range(lenLk):
            for j in range(i + 1, lenLk):
                if k > 2:
                    if Lk[i] ^ Lk[j] in self.fk2:
                        retList.add(Lk[i] | Lk[j])
                else:
                    retList.add(Lk[i] | Lk[j])
        return retList

    def main(self):
        C1 = self.createC(self.dataSet)
        D = list(map(set, self.dataSet))
        L1, supportData = self.scanD(D, C1, self.minsup)
        print('L1=>', L1)
        # print(supportData)
        self.L = [L1]
        k = 2
        while (len(self.L[k - 2]) > 0):
            Ck = self.aprioriGen(self.L[k - 2], k)
            Lk, supK = self.scanD(D, Ck, self.minsup)
            print("L%d=>" % k, Lk)
            supportData.update(supK)
            self.L.append(Lk)
            if k == 2:
                self.fk2 = Lk
            k += 1
        return self.L, supportData


class Apriori:
    def __init__(self, minsup, dataSet=None):
        self.dataSet = dataSet if dataSet else self.loadDataSet()
        self.minsup = minsup

    def loadDataSet(self):
        return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
        # return [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]

    # 找出所有的单个项
    def createC(self, dataset):
        C = []
        for data in dataset:
            for a in data:
                if not [a] in C:
                    C.append([a])
        return list(map(frozenset, C))

    # 扫描数据库，获取所有的频繁项集，和其支持度，这个里面的支持度是百分比计算的
    # 需要注意的是D和Ck里面的元素都是集合
    def scanD(self, D, Ck, minSupport):
        ssCnt = {}
        for tid in D:
            for can in Ck:
                if can.issubset(tid):
                    if not can in ssCnt:
                        ssCnt[can] = 1
                    else:
                        ssCnt[can] += 1
        numItems = float(len(list(D)))
        # print("numItems=>",numItems)
        # retList=[]
        retList = set()
        supportData = {}
        for key in ssCnt:
            support = ssCnt[key] / numItems
            if support >= minSupport:
                # retList.insert(0,key)
                retList.add(key)
                supportData[key] = support

        return retList, supportData

    # 这个是根据频繁项集(k-1)-项集，找候选频繁k-项集
    # Lk是频繁k-1项集的集合
    def aprioriGen(self, Lk, k):
        # print(Lk)
        retList = set()
        lenLk = len(Lk)
        Lk = list(Lk)
        for i in range(lenLk):
            for j in range(i + 1, lenLk):
                L1 = list(Lk[i])
                L2 = list(Lk[j])
                L1.sort()
                L2.sort()
                if L1[:k - 2] == L2[:k - 2]:
                    Ck_item = Lk[i] | Lk[j]
                    if self.filterCk(Ck_item, Lk):
                        retList.add(Ck_item)
        return retList

    def filterCk(self, Ck_item, Lksub1):
        for item in Ck_item:
            subCk = Ck_item - frozenset({item})
            if subCk not in Lksub1:
                return False
        return True

    def main(self):
        C1 = self.createC(self.dataSet)
        D = list(map(set, self.dataSet))
        L1, supportData = self.scanD(D, C1, self.minsup)
        # print('L1=>', L1)
        # print(supportData)
        L = [L1]
        k = 2
        while (len(L[k - 2]) > 0):
            Ck = self.aprioriGen(L[k - 2], k)
            Lk, supK = self.scanD(D, Ck, self.minsup)
            # print("L%d=>" % k, Lk)
            supportData.update(supK)
            L.append(Lk)
            k += 1
        return L, supportData


from collections import OrderedDict



# 一个递归树
# 每个child都是一个同样的SortedTree树
class SortedTree:
    def __init__(self, node, prefix, result, dataset=None):
        self.result = result
        self.node = node
        self.prefix = prefix
        self.support = 0
        self.children = []
        self.dataset = [] if not dataset else dataset

    def canLinked(self):
        # 真的是搞不懂，这个地方都可以有一个坑用来阻拦我
        return len(self.dataset) >= minSup

    # 给一个节点添加前缀，那么就是该节点的前缀，加上该节点的值
    def addChild(self, node):
        self.children.append(SortedTree(node, [node] + self.prefix, self.result))

    def addTransaction(self, transaction):
        self.dataset.append(transaction)

    def index(self, mark):
        return mark[self.node]

    def linking_depth_first(self, mark):
        """
        这个函数的部分可不可以再优化优化，这个可能需要的时间太长了
        直接找到所有index中最大的那个1
        这个以后得想想怎么优化
        这个不优化会不会比Apriori算法的结果更好呢？
        优化之后会不会更好呢？
        不优化应该也是比Apriori算法的结果更好的
        因为一个频繁项集, 统计支持度的话，需要统计k * N(N是指事务记录的总数)
        而在此算法中计算支持度的话，需要的时间为 k * M(M指的是父节点包含的记录总数)
        经过层层递进，M是越来越小的。也就是深度越深，支持度的时间是越少的
        这个地方写的还是有点问题的
        :return:
        """
        print("self.children is {}".format([child.node for child in self.children]))
        tmp = [(1 << child.index(mark)) for child in self.children]
        print("tmp is {}".format(tmp))
        """
        第一步，给每个孩子节点分数据
        """
        # 划分数据集
        for transaction in self.dataset:
            for ind, ttt in enumerate(tmp):
                if transaction & ttt == ttt:
                    self.children[ind].addTransaction(transaction)
                    # break

        """
        第二步，给每个孩子节点添加孩子节点
        """
        # 给该节点的每个孩子添加孩子节点
        # 通过该节点的孩子节点给孩子节点添加孩子节点的吗
        # 是不是应该通过该节点的兄弟节点
        for i in range(len(self.children) - 1):
            for j in range(i + 1, len(self.children)):
                self.children[i].addChild(self.children[j].node)

        self.support = len(self.dataset)
        del self.dataset
        """
        第三步，对孩子节点进行深度优先的挖掘
        """
        for child in self.children:
            # 目前暂时的策略就是超过频繁项基，才可以继续挖掘子节点
            # 但是呢，这个样子会过多的筛选不必要的候选项基
            if len(child.dataset) >= minSup:
                self.result.append(child.node + ', ' + self.prefix)
            else:
                continue
            print("prefix is {}".format(self.prefix))
            print("node is {}".format(child.node))
            print("dataset is {}".format([bin(transaction) for transaction in child.dataset]))
            print("child.children.length {}".format(len(child.children)))
            print("****" * 10)
            if child.canLinked():
                child.linking(mark)

    # 这一部分的计算通过广度优先的策略
    def linking_width_first(self, mark):
        """
        统计该节点每个孩子节点的支持度，对于满足支持度的进行连接和剪枝
        然后在进行下一步的计算
        :return:
        """
        # print("self.children is {}".format([child.node for child in self.children]))
        tmp = [(1 << child.index(mark)) for child in self.children]
        # print("tmp is {}".format(tmp))
        """
        第一步，给每个孩子节点分数据
        """
        # 划分数据集
        for transaction in self.dataset:
            for ind, ttt in enumerate(tmp):
                if transaction & ttt == ttt:
                    self.children[ind].addTransaction(transaction)
                    # break

        """
        第二步，筛选不是频繁项集的子节点
        """
        cur = 0
        while cur < len(self.children):
            if len(self.children[cur].dataset) < minSup:
                self.children.pop(cur)
            else:
                cur += 1
        # 给该节点的每个孩子添加孩子节点
        # 通过该节点的孩子节点给孩子节点添加孩子节点的吗
        # 是不是应该通过该节点的兄弟节点
        for i in range(len(self.children) - 1):
            for j in range(i + 1, len(self.children)):
                self.children[i].addChild(self.children[j].node)

        self.support = len(self.dataset)
        del self.dataset
        """
        第三步，对孩子节点进行深度优先的挖掘
        """
        for child in self.children:
            # 目前暂时的策略就是超过频繁项基，才可以继续挖掘子节点
            # 但是呢，这个样子会过多的筛选不必要的候选项基
            # print("prefix is {}".format(self.prefix))
            # print("node is {}".format(child.node))
            # print("dataset is {}".format([bin(transaction) for transaction in child.dataset]))
            # print("child.children.length {}".format(len(child.children)))
            # print("****" * 10)
            if child.canLinked():
                self.result.append([child.node] + self.prefix)
                child.linking_width_first(mark)


# 下一步，执行编码的操作
# 这个可以交给之前的代码来实现
# 然后就是完善频繁项基的步骤
# 明天争取跑出一个版本来
class Best_Encoded:
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
        return [['1', '3', '4'], ['2', '3', '5'], ['1', '2', '3', '5'], ['2', '5'], ['2', '3', '1']]
        # return [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]

    def scanDataset(self):
        for items in self.dataset:
            for item in items:
                self.mark[item] = self.mark.get(item, 0) + 1
        for item, support in list(self.mark.items()):
            # 感觉自己就像个傻逼一样，无药可救的很
            if support < minSup:
                del self.mark[item]
        # 从小到大排列的
        self.res = sorted(self.mark, key=lambda x: self.mark[x], reverse=True)
        self.fk_1 = self.mark
        print("fk_1 is {}".format(self.fk_1))
        self.mark = {node: (len(self.res) - ind - 1) for ind, node in enumerate(self.res)}

    # 这个地方fk1，看情况应该是从大到小排序就可以正确的编码了
    # 因为值是从小到大进行排列
    # 从后又从前到后的判断
    # 前面的移动的位次是最多的
    def encode(self, fk1, data):
        print("data is {}".format(data))
        print("fk1 is {}".format(fk1))
        encodedAffair = []
        for a in data:
            tmp = 0
            for ele in fk1:
                tmp = (tmp << 1) + 1 if ele in a else tmp << 1
            # 实际上的运算还是得用这个
            encodedAffair.append(tmp)
            # 这个可以用来做视觉上的展示
            # res.append(bin(tmp))
        return encodedAffair

    def main(self):
        result = []
        self.scanDataset()
        # print("fk_1 is {}".format(self.fk_1))
        # encode传入的应该是按照频繁项集从小到大排序的数组
        data = self.encode(self.res, self.dataset)
        for d in data:
            print(bin(d))
        # print("length is {}".format(len(data)))
        # print("编码后的事务记录为{}".format([bin(d) for d in data]))
        # # 展示编码结果
        # return data
        root = SortedTree('root', [], result, data)
        # print("self.res is {}".format(self.res))
        # print("self.mark is {}".format(self.mark))
        # print("self.mark is {}".format(self.mark))
        for node in self.res:
            root.addChild(node)
        if root.canLinked():
            root.linking_width_first(self.mark)
        print(result)
        print(len(result))


class SortedTree_NoneEncoded:
    def __init__(self, node, prefix, result, dataset=None):
        self.result = result
        self.node = node
        self.prefix = prefix
        self.support = 0
        self.children = []
        self.dataset = [] if not dataset else dataset

    def canLinked(self):
        # 真的是搞不懂，这个地方都可以有一个坑用来阻拦我
        return len(self.dataset) >= minSup

    # 给一个节点添加前缀，那么就是该节点的前缀，加上该节点的值
    def addChild(self, node):
        self.children.append(SortedTree_NoneEncoded(node, [self.node] + self.prefix, self.result))

    def addTransaction(self, transaction):
        self.dataset.append(transaction)


    # 这一部分的计算通过广度优先的策略
    def linking_width_first(self):
        """
        统计该节点每个孩子节点的支持度，对于满足支持度的进行连接和剪枝
        然后在进行下一步的计算
        :return:
        """
        """
        第一步，给每个孩子节点分数据
        """
        # 划分数据集
        for transaction in self.dataset:
            for ind, child in enumerate(self.children):
                if child.node in transaction:
                    self.children[ind].addTransaction(transaction)

        """
        第二步，筛选不是频繁项集的子节点
        """
        cur = 0
        while cur < len(self.children):
            if len(self.children[cur].dataset) < minSup:
                self.children.pop(cur)
            else:
                cur += 1
        # 给该节点的每个孩子添加孩子节点
        # 通过该节点的孩子节点给孩子节点添加孩子节点的吗
        # 是不是应该通过该节点的兄弟节点
        for i in range(len(self.children) - 1):
            for j in range(i + 1, len(self.children)):
                self.children[i].addChild(self.children[j].node)

        self.support = len(self.dataset)
        del self.dataset
        """
        第三步，对孩子节点进行深度优先的挖掘
        """
        for child in self.children:
            # 目前暂时的策略就是超过频繁项基，才可以继续挖掘子节点
            # 但是呢，这个样子会过多的筛选不必要的候选项基
            if child.canLinked():
                self.result.append([child.node] + self.prefix)
                child.linking_width_first()

class Best_NoneEncoded:
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
        for item, support in list(self.mark.items()):
            # 感觉自己就像个傻逼一样，无药可救的很
            if support < minSup:
                del self.mark[item]

    def main(self):
        result = []
        self.scanDataset()
        # print("length is {}".format(len(data)))
        # print("编码后的事务记录为{}".format([bin(d) for d in data]))
        # # 展示编码结果
        # return data
        root = SortedTree_NoneEncoded('root', [], result, [set(data) for data in self.dataset])
        # print("self.res is {}".format(self.res))
        print("self.mark is {}".format(self.mark))
        # print("self.mark is {}".format(self.mark))
        # 相当于给根节点添加孩子节点
        for node in self.mark:
            root.addChild(node)
        # 查看根节点是否满足条件
        if root.canLinked():
            root.linking_width_first()
        print(result)
        print(len(result))

def test(p, dataSet, minsup):
    start = time.time()
    ins = p(dataSet, minsup)
    ins.main()
    return time.time() - start


def loadDataset(path):
    dataset = []
    count1 = count2 = 0
    with open(path, 'r') as file:
        for line in file:
            # print(line.strip().split(','))
            # if line.strip().split(',')[-1] == '不合格':
            #     count1 += 1
            #     # continue
            #     dataset.append(line.strip().split(','))
            # elif line.strip().split(',')[-1] == '合格':
            #     count2 += 1
            #     # dataset.append(line.strip().split(','))
            # if line.strip().split(',')[-1] in ('合格', '不合格'):
            #     dataset.append(line.strip().split(','))
            dataset.append(line.strip().split(" "))
    # print("不合格的数量为{}".format(count1))
    # print("合格的数量为{}".format(count2))
    global minSup
    minSup = len(dataset) * 0.2
    return dataset

def generate_big_rules(L, support_data, min_conf):
    """
    Generate big rules from frequent itemsets.
    Args:
        L: The list of Lk.
        support_data: A dictionary. The key is frequent itemset and the value is support.
        min_conf: Minimal confidence.
    Returns:
        big_rule_list: A list which contains all big rules. Each big rule is represented
                       as a 3-tuple.
    """
    big_rule_list = []
    # 这个sub_set_list是用来干什么的？？？
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf, support_data[freq_set])
                    if conf >= min_conf and big_rule not in big_rule_list:
                        # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list

"""
下一步给节点加孩子，怎么给节点加孩子呢？
"""

if __name__ == '__main__':
    import sys
    # loadDataset(r'C:\Users\shichang.hu\Desktop\mushroom.dat.txt')
    start = time.time()
    # a = Apriori(0.005, dataSet=loadDataset(r"/Users/hushichang/Desktop/no_special_processed.csv"))
    # a = Apriori(0.2, dataSet=loadDataset(r"/Users/hushichang/mushroom.dat.txt"))
    a = Apriori(0.85, dataSet=loadDataset(r"/Users/hushichang/chess.dat"))
    # print("size is {}".format(sys.getsizeof(a)))
    L, support_data = a.main()
    print("length is {}".format(len(support_data)))
    print("cost time is {}".format(time.time() - start))
    # print(support_data)
    # for item in generate_big_rules(L, support_data, 0.8):
    #     if frozenset({'合格'}) == item[-3]:
    #         print(item)
    # print('res is {}'.format(res[0]))
    # b = Best(0.2, dataset=loadDataset(r'C:\Users\shichang.hu\Desktop\mushroom.dat.txt'))
    # b = Best_Encoded(0.2)
    # b = Best_Encoded(0.2, dataset=loadDataset(r'/Users/hushichang/mushroom.dat.txt'))
    # b = Best_Encoded(0.2)
    # b = Best_Encoded(0.4)
    # res = b.main()
    # print('cost time is {}'.format(time.time() - start))
