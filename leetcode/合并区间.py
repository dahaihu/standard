class Solution:
    def merge(self, intervals):
        """
        :type intervals: List[Interval]
        :rtype: List[Interval]
        """
        intervals.sort(key=lambda ele: (ele[0], ele[1]))
        i, j = 0, 1
        res = []
        while j < len(intervals):
            # 终点小于起点
            if intervals[i][1] < intervals[j][0]:
                res.append(intervals[i])
                i, j = j, j+1
            # 终点小于终点
            elif intervals[i][1] < intervals[j][1]:
                intervals[j] = [intervals[i][0], intervals[j][1]]
                i, j = j, j+1
            # 终点大于终点
            else:
                j = j + 1
        res.append(intervals[-1])
        return res

s = Solution()
print(s.merge([[1,4],[4,5]]))
# print(s.merge([[1,3],[2,6],[8,10],[15,18]]))



