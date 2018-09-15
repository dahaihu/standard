class Solution:
    """
    每个人做自己的事，不能越权，也不能不做好自己
    """
    def __init__(self):
        self.count = 0

    def solve(self, n):
        nums = [0 for _ in range(n)]
        self.dfs(nums, 0)
        return self.count

    def valid(self, nums, cur, ele):
        for i in range(cur):
            if nums[i] == ele or cur - i == abs(ele - nums[i]):
                return False
        return True

    def dfs(self, nums, cur):
        if cur == len(nums):
            self.count += 1
        else:
            for i in range(len(nums)):
                if self.valid(nums, cur, i):
                    nums[cur] = i
                    self.dfs(nums, cur+1)


s = Solution()
print(s.solve(8))
