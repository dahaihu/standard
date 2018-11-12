class Solution:
    def minDistance(self, word1, word2):
        """
        word1 -> word2
        :type word1: str
        :type word2: str
        :rtype: int
        """
        m, n = len(word1), len(word2)
        mark = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
        for i in range(1, m + 1):
            mark[0][i] = i
        for j in range(1, n + 1):
            mark[j][0] = j
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if word1[j - 1] == word2[i - 1]:
                    mark[i][j] = mark[i - 1][j - 1]
                else:
                    mark[i][j] = 1 + min(mark[i - 1][j - 1], mark[i - 1][j], mark[i][j - 1])
        return mark[-1][-1]


word1 = 'horse'
word2 = 'ros'
s = Solution()
print(s.minDistance(word1, word2))
