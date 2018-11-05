class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def reverse(head):
    """
    反转链表
    :param head:
    :return:
    """
    pre = None
    while head:
        head.next, head, pre = pre, head.next, head
    return pre


def addList(h1, h2):
    """
    链表表示的整数求和
    :param h1: 链表的头结点
    :param h2: 链表的头结点
    :return:
    """
    h1, h2 = reverse(h1), reverse(h2)
    carry = 0
    pre = None
    while h1 or h2 or carry:
        tmp = (h1.val if h1 else 0) + (h2.val if h2 else 0) + carry
        carry, tmp = divmod(tmp, 10)
        # 创建一个新的节点
        cur = Node(tmp)
        # 更新pre
        cur.next, pre = pre, cur
        # 更新h1, h2
        h1 = h1.next if h1 else 0
        h2 = h2.next if h2 else 0
    return pre


# a = [2, 8, 4, 7, 1, 4]
# b = [8, 9, 3, 4, 2]
#
# h1 = pre1 = Node(a[0])
# for ele in a[1:]:
#     pre1.next = Node(ele)
#     pre1 = pre1.next
#
# h2 = pre2 = Node(b[0])
# for ele in b[1:]:
#     pre2.next = Node(ele)
#     pre2 = pre2.next
#
# res = addList(h1, h2)
#
# while res:
#     print(res.val)
#     res = res.next


