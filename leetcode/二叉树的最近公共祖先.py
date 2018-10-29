"""
给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

例如，给定如下二叉树:  root = [3,5,1,6,2,0,8,null,null,7,4]

        _______3______
       /              \
    ___5__          ___1__
   /      \        /      \
   6      _2       0       8
         /  \
         7   4

"""


class Solution:
    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """
        pass

    def func(self, root, p, q):
        if root in (None, p, q):
            return root
        left, right = (self.func(kid, p, q) for kid in (root.left, root.right))
        return root if left and right else left or right

    def lowestCommonAncestor1(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """
        markleft = self.help(root, p, [])
        markright = self.help(root, q, [])
        mn = min(len(markleft), len(markright))
        for i in range(mn - 1, -1, -1):
            if markleft[i] == markright[i]:
                return markleft[i]

    # 感觉写成这样，才算真的理解了精髓
    # 返回一个节点的全部前缀
    # 你这个和上面的思路完全不一样，别给带偏了
    def help(self, root, node, mark):
        if not root:
            return
        tmp = mark + [root]
        if root.val == node.val:
            return tmp
        # tmpleft = self.help(root.left, node, tmp)
        # if tmpleft:
        #     return tmpleft
        # tmpright = self.help(root.right, node, tmp)
        # if tmpright:
        #     return tmpright
        return self.help(root.left, node, tmp) or self.help(root.right, node, tmp)
