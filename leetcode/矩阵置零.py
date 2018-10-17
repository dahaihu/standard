class Solution(object):
    def setZeroes(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: void Do not return anything, modify matrix in-place instead.
        """
        mark = []
        m, n = len(matrix), len(matrix[0])
        print(m, n)
        for i in range(m):
            for j in range(n):
                print("m is {}, n is {}".format(m, n))
                print('matrix is {}'.format(matrix))
                if matrix[i][j] == 0:
                    mark.append([i, j])
        print(mark)
        ind = {ele[0] for ele in mark}
        column = {ele[1] for ele in mark}
        for i in ind:
            for j in range(n):
                matrix[i][j] = 0
        for j in column:
            for i in range(m):
                matrix[i][j] = 0
        return


matrix = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]

s = Solution()
s.setZeroes(matrix)
print(matrix)