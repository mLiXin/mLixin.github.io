---
title: LeetCode.面试题55-I-二叉树的深度
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-04-15 10:40:53
---
###### Question
- Source
	- [面试题55 - I. 二叉树的深度](https://leetcode-cn.com/problems/er-cha-shu-de-shen-du-lcof/submissions/) 
- Title
	- 面试题55 - I. 二叉树的深度 
- Content
	- 输入一棵二叉树的根节点，求该树的深度。从根节点到叶节点依次经过的节点（含根、叶节点）形成树的一条路径，最长路径的长度为树的深度。
<!--more-->

###### Answer
- 思路
	- 递归即可 
- 时间复杂度
	- O(logN) 	
- 代码实现

	```Java
	public int maxDepth(TreeNode root) {
        if(root == null){
            return 0;
        }

        return 1 + Math.max(maxDepth(root.left),maxDepth(root.right));
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :39.6 MB, 在所有 Java 提交中击败了100.00%的用户
