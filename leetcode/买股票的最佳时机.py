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
                tmp_min = min(tmp_min, prices[i] - dp[k - 1][i - 1])
                dp[k][i] = max(dp[k][i - 1], prices[i] - tmp_min)
        return dp[-1][-1]
