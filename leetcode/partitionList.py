class Solution:
    def partition(self, head, x):
        pre = None
        res = right = head
        while head:
            if head.val < x:
                if right is head:
                    pre, head, right = head, head.next, head.next
                else:
                    if pre is None:
                        head.next, res, head, pre, right.next = res, head, head.next, head, head.next
                        continue
                    head.next, pre.next, right.next, head, pre = pre.next, head, head.next, head.next, head
            else:
                right, head = head, head.next
        return res

