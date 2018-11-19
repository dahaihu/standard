"""
给定一个整数数组 nums ，找出一个序列中乘积最大的连续子序列（该序列至少包含一个数）。

示例 1:

输入: [2,3,-2,4]
输出: 6
解释: 子数组 [2,3] 有最大乘积 6。
示例 2:

输入: [-2,0,-1]
输出: 0
解释: 结果不能为 2, 因为 [-2,-1] 不是子数组。

"""


class Solution:
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        mx = float('-inf')
        table = [[0 for _ in range(len(nums))] for _ in range(len(nums))]
        for i in range(len(nums)):
            table[0][i] = nums[i]
            mx = max(table[0][i], mx)
        # length + 1 为长度
        for length in range(1, len(nums)):
            for i in range(len(nums) - length):
                table[length][i] = table[length - 1][i] * nums[length + i]
                mx = max(table[length][i], mx)
        return mx

    def standard(self, nums):
        premx = premn = mx = nums[0]
        for ele in nums[1:]:
            if ele < 0:
                premx, premn = premn, premx
            premx = max(ele, premx * ele)
            premn = min(ele, premn * ele)
            mx = max(premx, mx)
        return mx


s = Solution()
print(s.standard([-2, 5, -1]))
