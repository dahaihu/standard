# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def getIntersectionNode(self, headA, headB):
        """
        :type head1, head1: ListNode
        :rtype: ListNode
        """
        rev_headA = self.reverseList(headA)
        rev_headB = self.reverseList(headB)
        tmp = None
        while rev_headA and rev_headB:
            if not rev_headA.val == rev_headB:
                # 如果不存在，将结果保存
                tmp = rev_headA
        if not tmp:
            return
        headA = self.reverseList(rev_headA)
        headB = self.reverseList(rev_headB)
        return tmp

    def reverseList(self, head):
        pre = None
        while head:
            pre, head.next, head = head, pre, head.next
        return head
