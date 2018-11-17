"""
峰值元素是指其值大于左右相邻值的元素。

给定一个输入数组 nums，其中 nums[i] ≠ nums[i+1]，找到峰值元素并返回其索引。

数组可能包含多个峰值，在这种情况下，返回任何一个峰值所在位置即可。

你可以假设 nums[-1] = nums[n] = -∞。

示例 1:

输入: nums = [1,2,3,1]
输出: 2
解释: 3 是峰值元素，你的函数应该返回其索引 2。
示例 2:

输入: nums = [1,2,1,3,5,6,4]
输出: 1 或 5
解释: 你的函数可以返回索引 1，其峰值元素为 2；
     或者返回索引 5， 其峰值元素为 6。
"""

"""
一个问题能不能转化为这个问题的子问题
不要想的那么复杂
现在基本上没有什么题是你没见过的
你要用脑子想
不要多做题
要多想题
找跟之前做过的题是否有关系
"""


class Solution:
    def findPeakElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        return self.help(nums, 0, len(nums) - 1)

    def help(self, nums, left, right):
        if left == right:
            return left
        mid1 = (left + right) // 2
        mid2 = mid1 + 1
        if nums[mid1] > nums[mid2]:
            return self.help(nums, left, mid1)
        return self.help(nums, mid2, right)
