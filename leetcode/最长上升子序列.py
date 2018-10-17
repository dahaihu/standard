"""
给定一个无序的整数数组，找到其中最长上升子序列的长度。

示例:

输入: [10,9,2,5,3,7,101,18]
输出: 4
解释: 最长的上升子序列是 [2,3,7,101]，它的长度是 4。
说明:

可能会有多种最长上升子序列的组合，你只需要输出对应的长度即可。
你算法的时间复杂度应该为 O(n2) 。
进阶: 你能将算法的时间复杂度降低到 O(n log n) 吗?
"""


class Solution(object):
    def lengthOfLIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        dp = [(nums[0], 1)]
        for ele in nums[1:]:
            tmp_mx = 1
            for items in dp:
                if items[0] >= ele:
                    tmp_mx = max(items[1] + 1, tmp_mx)
            dp.append((ele, tmp_mx))
        print(dp)
        return max([ele[1] for ele in dp])


nums = [10, 9, 2, 5, 3, 7, 101, 18]
s = Solution()
print(s.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]))
