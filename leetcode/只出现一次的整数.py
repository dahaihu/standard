class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        res = [0 for _ in range(32)]
        for i in range(32):
            for ele in nums:
                if ele & (2 ** i) == pow(2, i):
                    res[i] += 1
        res = [ele % 3 for ele in res]
        result = 0
        if res[-1] == 0:
            for ind, ele in enumerate(res):
                if ele == 1:
                    result |= 2 ** ind
            return result
        else:
            for ind, ele in enumerate(res[:-1]):
                if ele == 0:
                    result |= 2 ** ind
            return -(result + 1)


# nums = [2, 2, 3, 2]
nums = [-2, -2, 1, 1, -3, 1, -3, -3, -4, -2]
s = Solution()
print(s.singleNumber(nums))
