class Solution(object):
    def getPermutation(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """
        mark = [i for i in range(1, n+1)]
        table = [1 for _ in range(n)]
        for i in range(1, n):
            table[i] = i * table[i-1]
        res = ''
        k -= 1
        # while n > 0:
        while mark:
            ind, k = divmod(k, table[n-1])
            res += str(mark.pop(ind))
            n -= 1
        return res


s = Solution()

print(s.getPermutation(4, 9))
