class Solution:
    def longestPalindrome(self, s):
        # new_nums = '!#' + '#'.join(nums) + '#$'
        nums = list(s)
        # 索引的话，为什么就一定要想着是列表呢？ 你个傻子
        new_nums = '!#' + '#'.join(nums) + '#$'
        print('new_nums is {}'.format(new_nums))
        mark = [0 for _ in range(len(new_nums))]
        mxRight = 0
        pos = 0
        mx = 0
        for i in range(1, len(new_nums)-1):
            if i < mxRight:
                # if mark[2*pos-i] < mxRight - i:
                mark[i] = min(mark[2 * pos - i], mxRight - i)
                    # while new_nums[i - mark[i]] == new_nums[i + mark[i]]:
                    #     mark[i] += 1
            # else:
            # 在确定加1的情况下，再进行加一
            while new_nums[i - mark[i] - 1] == new_nums[i + mark[i] + 1]:
                mark[i] += 1
            # mark[i] -= 1
            print("i is {}, mark[i] is {}".format(new_nums[i], mark[i]))
            if mark[i] + i > mxRight:
                mxRight = mark[i] + 1
                # 这个pos去掉，在leetcode上面的结果也是对的
                pos = i
            if mx < mark[i]:
                mx = mark[i]
                res = new_nums[i-mark[i]:i+mark[i]+1]
        print(mark)
        return ''.join([ele for ele in res if ele != '#'])





s = Solution()
print(s.longestPalindrome('abba'))

