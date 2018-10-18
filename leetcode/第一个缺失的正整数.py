class Solution:
    # 为什么不能nums这样赋值呢？
    # nums[nums[i]] = nums[i]呢
    # 例如 如果数组中存在3 那么我们可不可以nums[3] = 3呢？
    # 这样最后的结果会不会和 [0, 1, 2, 3, 4, 5,,,]吗
    # 然后对这个数组从1开始遍历不就好了吗
    def firstMissingPositive(self, nums):
        nums.append(0)
        n = len(nums)
        for i in range(n):
            if nums[i] < 0 or nums[i] >= n:
                nums[i] = 0
        for i in range(n):
            nums[nums[i] % n] += n
        for i in range(1, n):
            if nums[i] < n:
                return i
        return n
