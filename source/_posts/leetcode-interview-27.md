---
title: LeetCode.面试题27-二叉树的镜像
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-04-10 11:17:28
---
###### Question
- Source
	- [面试题27. 二叉树的镜像](https://leetcode-cn.com/problems/er-cha-shu-de-jing-xiang-lcof/submissions/) 
- Title
	- 面试题27. 二叉树的镜像 
- Content
	- 请完成一个函数，输入一个二叉树，该函数输出它的镜像。 
<!--more-->

###### Answer
- 思路
	- 左右子树互换而已
- 时间复杂度
	- O(logN) 	
- 代码实现

	```Java
	public TreeNode mirrorTree(TreeNode root) {
        if(root == null){
            return null;
        }
        TreeNode leftTree = root.left;
        TreeNode rightTree = root.right;

        root.left = mirrorTree(rightTree);
        root.right = mirrorTree(leftTree);
        return root;
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :37.1 MB, 在所有 Java 提交中击败了100.00%的用户
