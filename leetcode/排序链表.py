"""
这个题目怎么能做出来呢

在 O(n log n) 时间复杂度和常数级空间复杂度下，对链表进行排序。

示例 1:

输入: 4->2->1->3
输出: 1->2->3->4
示例 2:

输入: -1->5->3->4->0
输出: -1->0->3->4->5
"""



# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def sortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        # 长度为0或者1 都返回head
        if not head or not head.next:
            return head
        pre = mid = right = head
        while right and right.next:
            pre = mid
            mid = mid.next
            right = right.next.next
        # 断绝两个链表的关系
        pre.next = None
        left = self.sortList(head)
        right = self.sortList(mid)
        return self.merge(left, right)

    def merge(self, h1, h2):
        if h1 and h2:
            if h1.val > h2.val:
                h1, h2 = h2, h1
            h1.next = self.merge(h1.next, h2)
        return h1 or h2
