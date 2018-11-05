"""
实现 strStr() 函数。

给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1。

示例 1:

输入: haystack = "hello", needle = "ll"
输出: 2
示例 2:

输入: haystack = "aaaaa", needle = "bba"
输出: -1

"""


class Solution(object):
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        # if not needle:
        #     return 0
        # length = 0
        # for i, ele in enumerate(haystack):
        #     if ele == needle[0]:
        #         ind = i
        #         while ind + length < len(haystack) and haystack[ind + length] == needle[length]:
        #             length += 1
        #             if length == len(needle):
        #                 return ind
        #         length = 0
        # return -1
        if not needle:
            return 0
        length = 0
        i = 0
        mark = self.help(needle)
        print('mark is {}'.format(mark))
        while i < len(haystack):
            # 开始匹配
            if haystack[i] == needle[length]:
                cur = i
                while i < len(haystack) and haystack[i + length] == needle[length]:
                    length += 1
                    if length == len(needle):
                        return cur
                i += mark[length - 1]
                length = 0
            else:
                i += 1
        return -1

    # 实现kmp算法的辅助工具
    def help(self, needle):
        """
        用来实现
        :param needle:
        :return:
        """
        return [self.func(needle[:i]) for i in range(1, len(needle) + 1)]

    def func(self, s):
        n = len(s)
        mx = 0
        for i in range(1, n):
            if s[:i] == s[-i:] and i > mx:
                mx = i
        return n - mx


s = Solution()

# print(s.strStr('hello', 'll'))
print(s.strStr('hello', 'll'))

