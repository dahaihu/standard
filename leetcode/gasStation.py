class Solution:
    def canCompleteCircuit(self, gas, cost):
        """
        :type gas: List[int]
        :type cost: List[int]
        :rtype: int
        """
        mark = list(map(lambda x, y: x-y, gas, cost))
        print(mark)
        if sum(mark) < 0:
            return -1
        NUM = len(mark)
        table = [[0 for _ in range(NUM)] for _ in range(NUM)]
        for i in range(NUM):
            table[i][0] = mark[i]
        # for ele in table:
        #     print(ele)
        for i in range(1, NUM):
            for j in range(NUM):
                table[j][i] = table[j][i-1] + mark[(i + j) % NUM]
        for ele in table:
            print("***" + str(ele))
        for ind, nums in enumerate(table):
            for ele in nums:
                if ele < 0:
                    break
            else:
                return ind
        return -1

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










s = Solution()
res = s.simplist([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
# print(res)

