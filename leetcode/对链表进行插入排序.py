# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def insertionSortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if not head:
            return
        if not head.next:
            return head
        pre = head
        head = head.next


dummy = head = ListNode(0)
a = [4, 1, 3, 2]
while a:
    tmp = ListNode(a.pop(0))
    dummy.next = tmp
    dummy = tmp

head = head.next

# while head:
#     print(head.val)
#     head = head.next

s = Solution()
res = s.insertionSortList(head)

while res:
    print(res.val)
    res = res.next
