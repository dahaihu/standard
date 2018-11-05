class Solution(object):
    def generateMatrix(self, n):
        """
        :type n: int
        :rtype: List[List[int]]
        """
        # 创建保存结果的矩阵
        self.res = [[0 for _ in range(n)] for _ in range(n)]
        self.help(0, 0, n, 1)
        return self.res

    def help(self, i, j, m, cur):
        """
        :param i: 起始点的横坐标
        :param j: 起始点的纵坐标
        :param m: 长度
        :param cur: 当前应该输入的值
        :return: None
        """
        # 上边界赋值
        print('i is {}, j is {}'.format(i, j))
        for x in range(m):
            self.res[i][j + x] = cur
            cur += 1
        if m == 1:
            return
        # 右边界赋值
        for y in range(1, m - 1):
            self.res[i + y][j + m - 1] = cur
            cur += 1
        # 下边界赋值
        for x in range(m - 1, -1, -1):
            self.res[i + m - 1][j + x] = cur
            cur += 1
        # 左边界赋值
        for y in range(m - 2, 0, -1):
            self.res[i + y][j] = cur
            cur += 1
        if m == 2:
            return
        self.help(i + 1, j + 1, m - 2, cur)


s = Solution()
for line in s.generateMatrix(4):
    print(line)
