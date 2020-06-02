---
title: LeetCode.面试题28-对称的二叉树
date: 2020-04-10 11:40:36
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
	- [面试题28. 对称的二叉树](https://leetcode-cn.com/problems/dui-cheng-de-er-cha-shu-lcof/) 
- Title
	- 面试题28. 对称的二叉树 
- Content
	- 请实现一个函数，用来判断一棵二叉树是不是对称的。如果一棵二叉树和它的镜像一样，那么它是对称的。
<!--more-->

###### Answer
- 思路
	- 镜像对称，则左子树的左子树和右子树的右子树需要相等，左子树的右子树和右子树的左子树需要相等。递归遍历即可。
- 时间复杂度
	- O(logN) 	
- 代码实现

	```Java
	public boolean isSymmetric(TreeNode root) {
        if(root == null){
            return true;
        }
        return isSymmetric(root.left,root.right);
    }

    public boolean isSymmetric(TreeNode left,TreeNode right){
        if(left == null && right == null){
            return true;
        }
        if(left == null || right == null || left.val != right.val){
            return false;
        }
        return isSymmetric(left.left,right.right) && isSymmetric(left.right,right.left);
     }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了36.37%的用户
	- 内存消耗 :37.7 MB, 在所有 Java 提交中击败了100.00%的用户
