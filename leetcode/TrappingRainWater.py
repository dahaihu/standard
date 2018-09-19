"""
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it is able to trap after raining.


The above elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped. Thanks Marcos for contributing this image!

Example:

Input: [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
"""

class Solution:
    def trap(self, height):
        left, right = 0, len(height)-1
        res = 0
        mxleft = mxright = 0
        while left < right:
            if height[left] < height[right]:
                if height[left] <= mxleft:
                    res += mxleft - height[left]
                else:
                    mxleft = height[left]
                left += 1
            else:
                if height[right] <= mxright:
                    res += mxright - height[right]
                else:
                    mxright = height[right]
                right -= 1
        return res
s = Solution()
print(s.trap([0,1,0,2,1,0,1,3,2,1,2,1]))
