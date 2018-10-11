import random

def help(nums1, nums2):
    res = []
    while nums1 and nums2:
        if nums1[0] <= nums2[0]:
            res.append(nums1.pop(0))
        else:
            res.append(nums2.pop(0))
    if nums1:
        res.extend(nums1)
    else:
        res.extend(nums2)
    return res

def sort(nums):
    if len(nums) == 1:
        return nums
    else:
        mid = len(nums)//2
        left = sort(nums[:mid])
        right = sort(nums[mid:])
        return help(left, right)

nums = list(range(10))
random.shuffle(nums)
print(sort(nums))