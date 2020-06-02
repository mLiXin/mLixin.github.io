---
title: LeetCode.096-Unique Binary Search Trees
date: 2019-10-28 11:15:47
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
	- [96. Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) 
- Title
	- 96. Unique Binary Search Trees 
- Content
	- Given n, how many structurally unique BST's (binary search trees) that store values 1 ... n?
<!--more-->

###### Answer
- 思路
	- 二叉搜索树，左子树都比root小，右子树都比root大，有n个升序的数，以任意第i个数为root，则前面的i-1个数为左子树，后面的n-i个数为右子树。左边有m种树，右边有n种树，则以第i个数为root的数有m*n种情况。遍历i从1到n即可
	- 实现可以递归遍历，也可以空间换时间的方式，因为有重复的情况。
- 时间复杂度
	- O(n2) 	
- 代码实现

	```Java
	public int numTrees(int n) {

        if (n == 0){
            return 1;
        }

        if (n==1){
            return 1;
        }
        int[] sumResult = new int[n + 1];
        sumResult[0] = 1;
        sumResult[1] = 1;

        for (int i = 2; i <= n; i++) {

            int sum = 0;
            for (int j = 1; j <= i; j++) {
                sum = sum + sumResult[j - 1] * sumResult[i - j];
            }

            sumResult[i] = sum;
        }

        return sumResult[n];
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Unique Binary Search Trees.
	- Memory Usage: 33.1 MB, less than 5.55% of Java online submissions for Unique Binary Search Trees.
