---
title: LeetCode.543-Diameter of Binary Tree
date: 2019-11-21 15:12:37
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
	- [543. Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) 
- Title
	- 543. Diameter of Binary Tree 
- Content
	- Given a binary tree, you need to compute the length of the diameter of the tree. The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root. 
<!--more-->

###### Answer
- 思路
	- 最长的直径就是左子树和右子树的深度之和，依次遍历就可以了。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	class Solution {
    	int max = 0;
    	public int diameterOfBinaryTree(TreeNode root) {
        	depth(root);
        	return max;
    	}

    	public int depth(TreeNode node) {
        	if (node == null) {
            	return 0;
        	}
        	int left = depth(node.left);
        	int right = depth(node.right);
        	max = Math.max(max, left + right);
        	return 1 + Math.max(left, right);
    	}
	}
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Diameter of Binary Tree.
	- Memory Usage: 38.4 MB, less than 46.75% of Java online submissions for Diameter of Binary Tree. 
