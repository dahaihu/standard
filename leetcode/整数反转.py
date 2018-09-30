# def func(value):
#     if value >= 0:
#         tmp, value = 1, value
#     else:
#         tmp, value = -1, -value
#     jin = 0
#     res = 0
#     while value:
#         yu, value = value % 10, value//10
#         res = res * 10 + yu
#         print(yu, value, res)
#         jin += 1
#     print(res if tmp > 0 else -res)

def func(n, m):
    nums = [[1 if i==0 else 0 for i in range(m + 1)] for _ in range(n + 1)]
    print(nums)
    for i in range(1, n+1):
        for j in range(1, m+1):
            if i <= j:
                nums[i][j] = nums[i-1][j]
            else:
                nums[i][j] = nums[i-1][j-i] + nums[i-1][j]
    for ele in nums:
        print(ele)
    return nums[-1][-1]
print(func(6, 8))




