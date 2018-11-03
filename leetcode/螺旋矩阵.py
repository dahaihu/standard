class Solution(object):
    def spiralOrder(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """
        self.res = []
        if not matrix or not matrix[0]:
            return []
        n, m = len(matrix), len(matrix[0])
        print('m is {m}, n is {n}'.format(m=m, n=n))
        self.help(0, 0, m, n, matrix)
        return self.res

    def help(self, i, j, m, n, matrix):
        """
        :param i: 起点的横坐标
        :param j: 起点的纵坐标
        :param m: 矩形的边缘长度
        :param n: 矩形的边缘宽度
        :param matrix: 数据提供的矩形
        :return:
        """
        if m == 0 or n == 0:
            return
        if m == 1:
            for y in range(i, i + n):
                self.res.append(matrix[y][j: j + m][0])
            return
        self.res.extend(matrix[i][j: j + m])
        if n == 1:
            return
        for x in range(1, n - 1):
            self.res.append(matrix[i + x][j: j + m][-1])
        self.res.extend(matrix[i + n - 1][j: j + m][::-1])
        for y in range(i + n - 1 - 1, i, -1):
            self.res.append(matrix[y][j: j + m][0])
        self.help(i + 1, j + 1, m - 2, n - 2, matrix)


matrix = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
s = Solution()
print(s.spiralOrder(matrix))
