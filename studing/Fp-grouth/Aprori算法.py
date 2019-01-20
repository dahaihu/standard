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
    def __init__(self, dataSet, minsup):
        self.dataSet = dataSet
        self.minsup = minsup

    def loadDataSet(self):
        # return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
        return [{'A', 'B', 'C', 'D'}, {'C', 'E'}, {'C', 'D'}, {'A', 'C', 'D'}, {'C', 'D', 'E'}]

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
        print('L1=>', L1)
        # print(supportData)
        L = [L1]
        k = 2
        while (len(L[k - 2]) > 0):
            Ck = self.aprioriGen(L[k - 2], k)
            Lk, supK = self.scanD(D, Ck, self.minsup)
            print("L%d=>" % k, Lk)
            supportData.update(supK)
            L.append(Lk)
            k += 1
        return L, supportData


from collections import OrderedDict

# mark 按照从小到大排序
mark = ['a', 'b', 'c', 'd', 'e']
mark.sort(reverse=True)


# 一个递归树
# 每个child都是一个同样的SortedTree树
class SortedTree:
    def __init__(self, node):
        self.node = node
        self.support = 0
        self.children = []
        self.dataset = []

    def canLinked(self):
        return len(self.children) >= 2

    def addChild(self, node):
        self.children.append(SortedTree(node))

    def addTransaction(self, transaction):
        self.dataset.append(transaction)

    def index(self, mark):
        return self.node.index(mark)

    def linking(self):
        """
        这个函数的部分可不可以再优化优化，这个可能需要的时间太长了
        直接找到所有index中最大的那个1
        这个以后得想想怎么优化
        这个不优化会不会比Apriori算法的结果更好呢？
        优化之后会不会更好呢？
        不优化应该也是比Apriori算法的结果更好的
        因为一个频繁项集, 统计支持度的话，需要统计k * N(N是指事务记录的总数)
        而在此算法中计算支持度的话，需要的时间为 k * M(M指的是父节点包含的记录总数)
        经过层层递进，M是越来越小的。也就是深度约深，支持度的时间是越少的
        :return:
        """
        tmp = [(1 << child.node.index(mark)) for child in self.children]
        for transaction in self.dataset:
            for ind, ttt in enumerate(tmp):
                if transaction & ttt == ttt:
                    self.children[ind].addTransaction(transaction)

    # 经过这个操作之后，再进行数dataset的遍历
    # 然后只遍历一次dataset就可以完成对dataset的分类
    def prev(self):
        self.mark = [(1 << child.index(mark)) for child in self.children]

    def getSupport(self):
        return len(self.dataset)


class Best:
    """
    dataset: 原始的数据集
    mark: 单项集 和 支持度， 以后的每个事务记录的排序都是根据这个进行排序

    """

    def __init__(self, dataset, minSup):
        self.dataset = dataset
        self.minSup = minSup
        self.mark = dict()
        self.res = dict()

    def scanDataset(self):
        for items in self.dataset:
            for item in items:
                self.mark[item] = self.mark.get(item, 0) + 1
        self.mark = {item: self.mark[item] for item in self.mark if self.mark[item] > self.minSup}


import time


# import pymysql
def test(p, dataSet, minsup):
    start = time.time()
    ins = p(dataSet, minsup)
    ins.main()
    return time.time() - start


def loadDataSet(num=1000):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='123456789',
        db='employees',
        port=3306,
        charset='utf8',
    )
    cur = conn.cursor()
    sql = 'select * from mushroom limit %d' % num
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [d[1:] for d in data]


if __name__ == '__main__':
    with open("mushroom.dat", 'r') as file:
        for line in file.readlines():
            print(line)
    # supL = [0.1, 0.15, 0.2, 0.25, 0.3]
    # pL = [BE_Apriori, AprioriP, Apriori]
    # data = loadDataSet()
    # result = []
    # for sup in supL:
    #     result.append([])
    #     for p in pL:
    #         result[-1].append(test(p, data, sup))
    # with open('result.txt','w') as file:
    #     file.write(str(result))
