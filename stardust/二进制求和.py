"""
给定两个二进制字符串，返回他们的和（用二进制表示）。

输入为非空字符串且只包含数字 1 和 0。

示例 1:

输入: a = "11", b = "1"
输出: "100"
示例 2:

输入: a = "1010", b = "1011"
输出: "10101"
"""


class Solution:
    def addBinary(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        carry = ''
        res = ''
        while a or b or carry:
            tmp = (int(a[-1]) if a else 0) + (int(b[-1]) if b else 0) + (1 if carry else 0)
            if tmp == 3:
                res = '1' + res
                carry = '1'
            elif tmp == 2:
                res = '0' + res
                carry = '1'
            else:
                res = str(tmp) + res
                carry = ''
            a = a[:-1] if a else ''
            b = b[:-1] if b else ''
        return res
