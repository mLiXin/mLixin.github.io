---
title: LeetCode.面试题54-二叉搜索树的第k大节点
date: 2020-04-15 11:10:50
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
	- [面试题54. 二叉搜索树的第k大节点](https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-di-kda-jie-dian-lcof/) 
- Title
	- 面试题54. 二叉搜索树的第k大节点 
- Content
	- 给定一棵二叉搜索树，请找出其中第k大的节点。 
<!--more-->

###### Answer
- 思路
	- 中序遍历，细节还可以优化
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int kthLargest(TreeNode root, int k) {
        // 中序遍历
        List<Integer> result = new ArrayList<>();
        mid(root,result);
        return result.get(result.size() - k);
    }

    public void mid(TreeNode root,List result){
        if(root.left != null){
            mid(root.left,result);
        }
        result.add(root.val);
        if(root.right != null){
            mid(root.right,result);
        }
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了62.29%的用户
	- 内存消耗 :39.8 MB, 在所有 Java 提交中击败了100.00%的用户
