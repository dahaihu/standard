"""
Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the area of largest rectangle in the histogram.


Above is a histogram where width of each bar is 1, given height = [2,1,5,6,2,3].




The largest rectangle is shown in the shaded area, which has area = 10 unit.



Example:

Input: [2,1,5,6,2,3]
Output: 10
"""

class Solution:
    def largestRectangleArea(self, heights):
        stack = []
        temp = []
        heights.append(-1)
        for ind, height in enumerate(heights):
            cur = ind
            while stack and stack[-1][-1] < height:
                cur, h = stack.pop()
                temp.append((ind - cur) * h)
            stack.append([cur, h])
        return max(temp) if temp else 0
