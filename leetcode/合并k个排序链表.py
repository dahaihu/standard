# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        lists = [ele for ele in lists if ele]
        # 第一次调整堆
        for i in range(len(lists) // 2 - 1, -1, -1):
            self.adjust(i, lists)
        head = dummy = ListNode(0)
        while lists:
            # 取出堆顶的元素
            head.next = lists[0]
            # 对堆顶的链表还为下一个元素
            head = head.next
            lists[0] = lists[0].next
            # 如果堆定元素为空，说明这个链表的元素已经全部插入到结果中
            # 那么用末尾元素进行替代
            if not lists[0]:
                lists[0] = lists[-1]
                lists = lists[:-1]
            # 调整堆定元素
            self.adjust(0, lists)
        return dummy.next

    # 这个是用来调整堆的，对堆定元素进行调整
    def adjust(self, i, lists):
        while 2 * i + 1 < len(lists):
            tmp = 2 * i + 1
            if tmp + 1 < len(lists) and lists[tmp].val > lists[tmp + 1].val:
                tmp += 1
            if lists[i].val <= lists[tmp].val:
                break
            lists[i], lists[tmp] = lists[tmp], lists[i]
            i = tmp
