class Solution:
    def subsetsWithDup(self, nums):
        nums.sort()
        results = [[]]
        for i in range(len(nums)):
            new_results = []
            for result in results:
                if i > 0 and nums[i] == nums[i - 1] and len(result) > 0 and result[-1] == nums[i]:
                    new_results.append(result + [nums[i]])
                    continue
                new_results.append(result + [nums[i]])
                new_results.append(result)
            results = new_results
        return results


class Standard:
    def subsetsWithDup(self, nums):
        nums.sort()
        res = [[]]
        for i in range(len(nums)):
            if i == 0 or nums[i] != nums[i - 1]:
                l = len(res)
            for j in range(len(res) - l, len(res)):
                res.append(res[j] + [nums[i]])
        return res


nums = [1, 2, 2]
s = Standard()
print(s.subsetsWithDup(nums))
