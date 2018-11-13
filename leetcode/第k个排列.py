class Solution(object):
    def getPermutation(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """
        mark = [i for i in range(1, n + 1)]
        res = 0
        table = [1]
        k -= 1
        for i in range(1, n):
            table.append(table[-1] * i)
        while mark:
            m, k = divmod(k, table.pop(-1))
            res = 10 * res + mark.pop(m)
        return str(res)


s = Solution()

print(s.getPermutation(3, 6))
