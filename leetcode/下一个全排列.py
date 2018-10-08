"""实现获取下一个排列的函数，算法需要将给定数字序列重新排列成字典序中下一个更大的排列。

如果不存在下一个更大的排列，则将数字重新排列成最小的排列（即升序排列）。

必须原地修改，只允许使用额外常数空间。

以下是一些例子，输入位于左侧列，其相应输出位于右侧列。
1,2,3 → 1,3,2
3,2,1 → 1,2,3
1,1,5 → 1,5,1
"""


class Solution:
    def nextPermutation(self, nums):
        """
        :type nums: List[int]
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        tmp = 0
        # 逆序遍历， 只到索引为1的
        for i in range(len(nums) - 1, 0, -1):
            print("i is {}".format(i))
            if nums[i] > nums[i - 1]:
                tmp = i
                print('i is {}, tmp is {}'.format(i, tmp))
                break
        else:
            left, right = 0, len(nums) - 1
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1
            return
        for i in range(len(nums) - 1, tmp - 1, -1):
            print("i is {}".format(i))
            if nums[i] > nums[tmp - 1]:
                nums[i], nums[tmp - 1] = nums[tmp - 1], nums[i]
                break
        right = len(nums) - 1
        while tmp < right:
            nums[tmp], nums[right] = nums[right], nums[tmp]
            tmp += 1
            right -= 1
