class Solution:
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        if len(prices) <= 1:
            return 0
        dp = [[0] * len(prices) for _ in range(3)]
        # for k in range(1,3):
        #     for i in range(1,len(prices)):
        #         tmp_mirices[0]
        #         for j in range(1,i):
        #             tmp_min=min(tmp_min,prices[j] - dp[k-1][j-1])
        #         dp[k][i]=max(dp[k][i-1],prices[i]-tmp_min)
        for k in range(1, 3):
            tmp_min = prices[0]
            for i in range(1, len(prices)):
                # 感觉这样分开算很是惨绝人寰的难易理解
                tmp_min = min(tmp_min, prices[i] - dp[k - 1][i - 1])
                dp[k][i] = max(dp[k][i - 1], prices[i] - tmp_min)
        return dp[-1][-1]


# 通过一次的来理解多次的计算方式
def once(nums):
    # dp = [0]
    # tmp_min = nums[0]
    # for i in range(1, len(nums)):
    #     # 要透过现象看本质
    #     tmp_min = min(tmp_min, nums[i])
    #     dp.append(nums[i] - tmp_min)
    # return max(dp)
    dp = [0 for _ in range(len(nums))]
    tmp_min = nums[0]
    for i in range(1, len(nums)):
        tmp_min = min(tmp_min, nums[i])
        dp[i] = max(nums[i] - tmp_min, dp[i - 1])
    return dp[-1]

nums = [7, 1, 5, 3, 6, 4]
print(once(nums))
