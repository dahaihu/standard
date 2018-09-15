class Solution:
    def simplist(self, gas, cost):
        mark = list(map(lambda x, y: x - y, gas, cost))
        print(mark)
        if sum(mark) < 0:
            return -1
        table = [0]
        for ele in mark:
            table.append(ele + table[-1])
        table = table[1:]
        for i in range(len(mark)):
            for ele in table:
                if ele < 0:
                    break
            else:
                return i
        return -1

    def canCompleteCircuit(self, gas, cost):
        """
        双指针的策略，
        这个题目怎么说呢，
        如果sum(mark) < 0 那么肯定无解
        如果sum(mark) >= 0 那么肯定有解
        而有解呢，就是走一圈。
        往前走不行的话，只能后退，始发地点可以的索引可以减1
        :param gas:
        :param cost:
        :return:
        """
        mark = list(map(lambda x, y: x - y, gas, cost))
        if sum(mark) < 0:
            return -1
        print(mark)
        i, j = 0, len(mark) - 1
        tmp = 0
        while i <= j:
            if tmp < 0:
                tmp += mark[j]
                j -= 1
            else:
                tmp += mark[i]
                i += 1
        return j+1 if j != len(mark)-1 else 0


gas = [2, 3, 4]
cost = [3, 4, 3]

# gas = [1, 2, 3, 4, 5]
# cost = [3, 4, 5, 1, 2]
s = Solution()
res = s.canCompleteCircuit(gas, cost)
print(res)
