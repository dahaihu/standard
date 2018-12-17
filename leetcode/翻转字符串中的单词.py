"""

给定一个字符串，逐个翻转字符串中的每个单词。

示例:

输入: "the sky is blue",
输出: "blue is sky the".
说明:

无空格字符构成一个单词。
输入字符串可以在前面或者后面包含多余的空格，但是反转后的字符不能包括。
如果两个单词间有多余的空格，将反转后单词间的空格减少到只含一个。
进阶: 请选用C语言的用户尝试使用 O(1) 空间复杂度的原地解法。
"""


class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        s = list(s)[::-1]
        left = right = 0
        while right < len(s):
            if s[right] != ' ':
                right += 1
                continue
            else:
                if left == right:
                    s.pop(left)
                    # while right < len(s) and s[right] == ' ':
                    #     left = right = right + 1
                else:
                    # print(''.join(s[right - 1: left - 1: -1]))
                    # res += ''.join(s[right - 1: left - 1: -1])
                    tmp = right
                    right = right - 1
                    while left < right:
                        s[left], s[right] = s[right], s[left]
                        left += 1
                        right -= 1
                    left = right = tmp + 1
        if left < len(s):
            right = right - 1
            while left < right:
                s[left], s[right] = s[right], s[left]
                left += 1
                right -= 1
        return ''.join(s).strip()


string = " the sky is  blue "
s = Solution()
print(s.reverseWords(string))
