class Solution:
    def containsDuplicate(self, nums):
        """
        要好好的理解需求，感觉自己的答案是对的话，就多读题
        仔细理解，和自己理解的差别
        :type nums: List[int]
        :rtype: bool
        """
        once = set()
        for ele in nums:
            if ele in once:
                return True
            else:
                once.add(ele)
        return False

s = Solution()
print(s.containsDuplicate([1, 2, 3, 1]))
