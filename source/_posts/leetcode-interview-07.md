---
title: LeetCode.面试题07-重建二叉树
date: 2020-03-30 18:37:25
tags:
- 数据结构与算法
- LeetCode
categories:
- 数据结构与算法
- LeetCode
visible: hide
---
###### Question
- Source
	- [面试题07. 重建二叉树](https://leetcode-cn.com/problems/zhong-jian-er-cha-shu-lcof/) 
- Title
	- 面试题07. 重建二叉树 
- Content
	- 输入某二叉树的前序遍历和中序遍历的结果，请重建该二叉树。假设输入的前序遍历和中序遍历的结果中都不含重复的数字。 
<!--more-->

###### Answer
- 思路
	- 递归实现，前序第一个值为root，中序队列root左边的数组是左子树，右边是右子树，依次递归遍历即可。
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	public TreeNode buildTree(int[] preorder, int[] inorder) {
        if (preorder == null || preorder.length == 0 || inorder == null || inorder.length == 0){
            return null;
        }
        return buildTree(preorder, inorder, 0, preorder.length - 1, 0, inorder.length - 1);

    }

    public TreeNode buildTree(int[] preOrder, int[] inOrder, int preOrderStart, int preOrderEnd,
            int inOrderStart, int inOrderEnd) {

        if (preOrderStart > preOrderEnd || inOrderStart > inOrderEnd) {
            return null;
        }

        int root = preOrder[preOrderStart];
        int inPos = inOrderStart;
        for (int i = inOrderStart; i <= inOrderEnd; i++) {
            if (inOrder[i] == root) {
                inPos = i;
            }
        }

        TreeNode result = new TreeNode(root);
        result.left = buildTree(preOrder, inOrder, preOrderStart + 1,
                preOrderStart + inPos - inOrderStart, inOrderStart, inPos - 1);
        result.right = buildTree(preOrder, inOrder, preOrderStart + 1 + inPos - inOrderStart,
                preOrderEnd, inPos + 1, inOrderEnd);
        return result;
    }
	```
- 提交结果
	- 执行用时 :4 ms, 在所有 Java 提交中击败了65.04%的用户
	- 内存消耗 :40.2 MB, 在所有 Java 提交中击败了100.00%的用户
