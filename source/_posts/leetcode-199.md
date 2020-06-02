---
title: LeetCode.199-Binary Tree Right Side View
date: 2019-10-28 11:45:44
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
	- [199. Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) 
- Title
	- 199. Binary Tree Right Side View 
- Content
	- Given a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.
<!--more-->

###### Answer
- 思路
	- 层序遍历，因为是从右边，所以可以变通一下，从右往左遍历，第一个就是右视图的数
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public List<Integer> rightSideView(TreeNode root) {

        List<Integer> result = new ArrayList<Integer>();
        levelHelper(root, result, 0);

        return result;
    }

    public void levelHelper(TreeNode root, List<Integer> result, int level) {
        if (root == null) {
            return;
        }
        if (result.size() == level) {
            result.add(root.val);
        }

        levelHelper(root.right, result, level + 1);
        levelHelper(root.left, result, level + 1);

    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 100.00% of Java online submissions for Binary Tree Right Side View.
	- Memory Usage: 35.4 MB, less than 100.00% of Java online submissions for Binary Tree Right Side View.
