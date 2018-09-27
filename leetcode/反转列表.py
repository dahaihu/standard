class Solution:

    def solve(self, head):
        pre = None
        while head:
            head.next, head, pre = pre, head.next, head
        return pre
