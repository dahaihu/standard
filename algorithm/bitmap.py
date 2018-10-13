class Bitmap(object):
    def __init__(self, max):
        self.size = self.calcElemIndex(max)
        self.array = [0 for _ in range(self.size + 1)]

    def calcElemIndex(self, num):
        """
        加 1 的原因是，数组中也可能包含 0
        所以应该向上取整
        :param num:
        :return:
        """
        # return int((num + 31 - 1) / 31)  # 向上取整
        return (num + 1) // 31

    def calcBitIndex(self, num):
        return num % 31

    def set(self, num):
        elemIndex = self.calcElemIndex(num)
        byteIndex = self.calcBitIndex(num)
        elem = self.array[elemIndex]
        # 为什么要用 | 这个的知道，
        # 这个可以表示集合的或
        # 还可以表示二进制的或
        self.array[elemIndex] = elem | (1 << byteIndex)

    def test(self, i):
        eleIndex = self.calcElemIndex(i)
        byteIndex = self.calcBitIndex(i)
        elem = self.array[eleIndex]
        return True if elem & (1 << byteIndex) == (1 << byteIndex) else False


nums = [45, 2, 78, 35, 67, 90, 879, 0, 340, 123, 46]
MAX = 879
bitmap = Bitmap(MAX)
for num in nums:
    bitmap.set(num)

result = []
for i in range(MAX + 1):
    if bitmap.test(i):
        result.append(i)

print(result)

