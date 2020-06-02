---
title: LeetCode.面试题32-II-从上到下打印二叉树 II
date: 2020-04-13 10:53:02
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
	- [面试题32 - II. 从上到下打印二叉树 II](https://leetcode-cn.com/problems/cong-shang-dao-xia-da-yin-er-cha-shu-ii-lcof/) 
- Title
	- 面试题32 - II. 从上到下打印二叉树 II 
- Content
	- 从上到下按层打印二叉树，同一层的节点按从左到右的顺序打印，每一层打印到一行。
	 
<!--more-->

###### Answer
- 思路
	- 递归实现
	- 如果是不拆分层数，不使用递归，可以通过队列实现 
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	List<List<Integer>> result = new ArrayList<>();
    public List<List<Integer>> levelOrder(TreeNode root) {
        if (root == null) {
            return new ArrayList<>();
        }

        levelOrder(root,1);
        return result;
    }

    public void levelOrder(TreeNode treeNode,int level){
        if (treeNode == null){
            return;
        }

        if (level > result.size()){
            result.add(new ArrayList<>());
        }
        result.get(level-1).add(treeNode.val);

        levelOrder(treeNode.left,level+1);
        levelOrder(treeNode.right,level+1);
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :40 MB, 在所有 Java 提交中击败了100.00%的用户
