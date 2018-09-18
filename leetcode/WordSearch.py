"""
给定一个二维网格和一个单词，找出该单词是否存在于网格中。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

示例:

board =
[
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
]

给定 word = "ABCCED", 返回 true.
给定 word = "SEE", 返回 true.
给定 word = "ABCB", 返回 false.
"""


class Solution:
    def __init__(self):
        self.m = self.n = 0

    def exist(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """
        if not board:
            return False
        self.m = len(board)
        if not board[0]:
            return False
        self.n = len(board[0])
        # # 这个还是垃圾代码的一部分
        # mark = list()
        for i in range(self.m):
            for j in range(self.n):
                if self.func(board, i, j, word):
                    return True
                # # 这个也是那个非常垃圾代码的一部分
                # if board[i][j] == word[0]:
                #     if not self.func(board, i, j, word[1:], mark + [(i, j)]):
                #         continue
                #     else:
                #         return True
        return False

    def func(self, board, i, j, word):
        if board[i][j] == word[0]:
            if not word[1:]:
                return True
            board[i][j] = ''
            if i < len(board)-1 and self.func(board, i+1, j, word[1:]):
                return True
            if i > 0 and self.func(board, i-1, j, word[1:]):
                return True
            if j < len(board[0])-1 and self.func(board, i, j+1, word[1:]):
                return True
            if j > 0 and self.func(board, i, j-1, word[1:]):
                return True
        else:
            return False
        # # 这个应该是我写的非常垃圾的代码了
        # if not word:
        #     return True
        # if i + 1 < self.m and word[0] == board[i + 1][j] and (i + 1, j) not in mark:
        #     if self.func(board, i + 1, j, word[1:], mark+[(i+1, j)]):
        #         return True
        # if i - 1 > -1 and word[0] == board[i - 1][j] and (i - 1, j) not in mark:
        #     if self.func(board, i - 1, j, word[1:], mark+[(i-1, j)]):
        #         return True
        # if j + 1 < self.n and word[0] == board[i][j + 1] and (i, j + 1) not in mark:
        #     if self.func(board, i, j + 1, word[1:], mark+[(i, j+1)]):
        #         return True
        # if j - 1 > -1 and word[0] == board[i][j - 1] and (i, j - 1) not in mark:
        #     if self.func(board, i, j - 1, word[1:], mark+[(i, j-1)]):
        #         return True


board = [
    ['A', 'B', 'C', 'E'],
    ['S', 'F', 'C', 'S'],
    ['A', 'D', 'E', 'E']
]
s = Solution()
print(s.exist(board, "ABCB"))
