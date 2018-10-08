"""实现获取下一个排列的函数，算法需要将给定数字序列重新排列成字典序中下一个更大的排列。

如果不存在下一个更大的排列，则将数字重新排列成最小的排列（即升序排列）。

必须原地修改，只允许使用额外常数空间。

以下是一些例子，输入位于左侧列，其相应输出位于右侧列。
1,2,3 → 1,3,2
3,2,1 → 1,2,3
1,1,5 → 1,5,1
"""


class Solution:
    """
    总结起来就是两步
    1. 找到需要调换元素的索引，进行调换
    2. 调换之后，后面得元素要逆序排列一下，生成交换后的最小值
    """
    def nextPermutation(self, nums):
        """
        :type nums: List[int]
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        tmp = 0
        # 逆序遍历， 只到索引为1的, 找到一个索引，这个索引i指向的元素值大于索引i-1所指向的元素值
        for i in range(len(nums) - 1, 0, -1):
            print("i is {}".format(i))
            if nums[i] > nums[i - 1]:
                tmp = i
                print('i is {}, tmp is {}'.format(i, tmp))
                break
        else:
            # 没有这个索引，就说明nums是根据大小逆序排列的，然后逆序回来即可
            left, right = 0, len(nums) - 1
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1
            return
        # 找到索引i之后的大于这个值得最小值，然后进行替换
        for i in range(len(nums) - 1, tmp - 1, -1):
            print("i is {}".format(i))
            if nums[i] > nums[tmp - 1]:
                nums[i], nums[tmp - 1] = nums[tmp - 1], nums[i]
                break
        # 替换完成之后，i之后的元素逆序排列一下，因为i之后的元素是从大到小排列的
        right = len(nums) - 1
        while tmp < right:
            nums[tmp], nums[right] = nums[right], nums[tmp]
            tmp += 1
            right -= 1
