"""
给定一个字符串 (s) 和一个字符模式 (p)。实现支持 '.' 和 '*' 的正则表达式匹配。

'.' 匹配任意单个字符。
'*' 匹配零个或多个前面的元素。
匹配应该覆盖整个字符串 (s) ，而不是部分字符串。

说明:

s 可能为空，且只包含从 a-z 的小写字母。
p 可能为空，且只包含从 a-z 的小写字母，以及字符 . 和 *。
示例 1:

输入:
s = "aa"
p = "a"
输出: false
解释: "a" 无法匹配 "aa" 整个字符串。
示例 2:

输入:
s = "aa"
p = "a*"
输出: true
解释: '*' 代表可匹配零个或多个前面的元素, 即可以匹配 'a' 。因此, 重复 'a' 一次, 字符串可变为 "aa"。
示例 3:

输入:
s = "ab"
p = ".*"
输出: true
解释: ".*" 表示可匹配零个或多个('*')任意字符('.')。
示例 4:

输入:
s = "aab"
p = "c*a*b"
输出: true
解释: 'c' 可以不被重复, 'a' 可以被重复一次。因此可以匹配字符串 "aab"。
示例 5:

输入:
s = "mississippi"
p = "mis*is*p*."
输出: false
"""
class Solution:
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        m, n = len(p), len(s)
        mark = [[False for _ in range(n + 1)] for _ in range(m + 1)]
        mark[0][0] = True
        # 分别对p和s长度为0时进行赋值
        # 因为后面矩阵进行求值的时候都要用到i-1,j-1或者i-2之类的
        # 不先赋值的话，后面得求值都会是错误的
        for i in range(1, m+1):
            if p[i-1] == '*':
                mark[i][0] = mark[i-2][0]
        for j in range(1, n+1):
            mark[0][j] = False
        # for ele in mark:
        #     print(ele)
        for i in range(1, m+1):
            for j in range(1, n+1):
                # 如果两者相等，那么取决于(i-1, j-1)
                # 而这个相等又有两种情况
                # 情况1 是两个字符是a-z的意义上的相等
                # 情况2 是p为'.'，就是当前的'.'可以匹配任意字符
                if p[i-1] == s[j-1] or p[i-1] == '.':
                    mark[i][j] = mark[i-1][j-1]
                # 这种情况下就有点点复杂了
                elif p[i-1] == '*':
                    # '*'前面的元素长度为1，或者为0
                    mark[i][j] = mark[i-2][j] or mark[i-1][j]
                    # '*'前面的元素的长度为多个，
                    # 这个多个也有两种情况
                    # 情况1 前面的元素为a-z意义上的多个
                    # 情况2 前面的元素为'.'意义上的多个
                    if p[i-2] == s[j-1] or p[i-2] == '.':
                        mark[i][j] |= mark[i][j-1]
        print('*' * 10)
        for ele in mark:
            print(ele)
        return mark[-1][-1]