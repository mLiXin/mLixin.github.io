---
title: LeetCode.面试题55-II-平衡二叉树
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-04-15 10:56:27
---
###### Question
- Source
	- [面试题55 - II. 平衡二叉树](https://leetcode-cn.com/problems/ping-heng-er-cha-shu-lcof/) 
- Title
	- 面试题55 - II. 平衡二叉树 
- Content
	- 输入一棵二叉树的根节点，判断该树是不是平衡二叉树。如果某二叉树中任意节点的左右子树的深度相差不超过1，那么它就是一棵平衡二叉树。 
<!--more-->

###### Answer
- 思路
	- 从顶向下，计算深度并比较即可 
- 时间复杂度
	- O(nLogN) 	
- 代码实现

	```Java
	public boolean isBalanced(TreeNode root) {
        if(root == null){
            return true;
        }
        return Math.abs(getDepth(root.left) - getDepth(root.right)) <=1 && isBalanced(root.left) && isBalanced(root.right);
    }

    public int getDepth(TreeNode root){
        if(root == null){
            return 0;
        }
        return 1 + Math.max(getDepth(root.left),getDepth(root.right));
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了99.97%的用户
	- 内存消耗 :39.6 MB, 在所有 Java 提交中击败了100.00%的用户
