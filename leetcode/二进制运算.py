def subSet1(nums):
    """
    通过二进制数的特性，求给定集合的子集
    :param nums:
    :return:
    """
    n = len(nums)
    res = []
    # 可以把这个i当成二进制数看待
    for i in range(2 ** n):
        tmp = []
        for j in range(n):
            if i & 2 ** j == 2 ** j:
                tmp.append(nums[j])
        res.append(tmp)
    return res


def subSet2(nums):
    res = [[]]
    for ele in nums:
        n = len(res)
        for i in range(n):
            res.append(res[i] + [ele])
    return res


print(subSet1([1, 2, 3, 4]))
print(subSet2([1, 2, 3, 4]))

def exchange(x, y):
    """
    不用额外的空间交换两个变量的值
    用到的异或的运算，有两个公式(相同为0， 不同为1)
    0 ^ a = a
    a ^ a = 0
    :param x:
    :param y:
    :return:
    """
    x ^= y
    y ^= x
    x ^= y
    return x, y


"""
给定两个整数，被除数 dividend 和除数 divisor。将两数相除，要求不使用乘法、除法和 mod 运算符。

返回被除数 dividend 除以除数 divisor 得到的商。

示例 1:

输入: dividend = 10, divisor = 3
输出: 3
示例 2:

输入: dividend = 7, divisor = -3
输出: -2
说明:

被除数和除数均为 32 位有符号整数。
除数不为 0。
假设我们的环境只能存储 32 位有符号整数，其数值范围是 [−231,  231 − 1]。本题中，如果除法结果溢出，则返回 231 − 1"""


class Solution:
    def divide(self, dividend, divisor):
        # 需要详细的知道每个参数的含义，才能正确的获取计算结果
        """
        :type dividend: int
        :type divisor: int
        :rtype: int
        """
        if divisor == 0:
            return pow(2, 31) - 1
        sign = 1 if divisor * dividend >= 0 else -1
        divisor = divisor if divisor >= 0 else -divisor
        dividend = dividend if dividend >= 0 else -dividend
        res = 0
        while dividend >= divisor:
            i = 0
            tmp = divisor
            while tmp <= dividend:
                tmp <<= 1
                i += 1
            print("i is {}, dividend is {}, tmp is {}".format(i, dividend, tmp))
            res += 1 << (i - 1)
            dividend -= (tmp >> 1)
        res *= sign
        if res >= -pow(2, 31) and res < pow(2, 31):
            return res
        else:
            return pow(2, 31) - 1


# s = Solution()
# print(s.divide(7, 3))
