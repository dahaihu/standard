# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def sortedListToBST(self, head):
        # 长度为0
        if not head:
            return
        # 长度为1
        if head and not head.next:
            return TreeNode(head.val)
        # # 长度为2
        # if head and head.next and not head.next.next:
        #     root = TreeNode(head.next.val)
        #     root.left = TreeNode(head.val)
        #     return root
        pre = mid = right = head
        while right and right.next:
            pre = mid
            mid = mid.next
            right = right.next.next
        pre.next = None
        root = TreeNode(mid.val)
        root.left = self.sortedListToBST(head)
        root.right = self.sortedListToBST(mid.next)
        return root
