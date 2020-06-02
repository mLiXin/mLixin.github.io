---
title: LeetCode.240-Search a 2D Matrix II
date: 2019-10-12 10:50:00
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
	- [240. Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/submissions/) 
- Title
	- 240. Search a 2D Matrix II 
- Content
	- Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:
		- Integers in each row are sorted in ascending from left to right.
		- Integers in each column are sorted in ascending from top to bottom.
<!--more-->

###### Answer
- 思路
	- 从右上角开始遍历，如果target小于该值，说明在该列左边；如果target大于该值，说明在该行下边；如果相等，则直接返回。
- 时间复杂度
	- O(logN) 	
- 代码实现

	```Java
	public boolean searchMatrix(int[][] matrix, int target) {
        if (matrix == null || matrix.length == 0){
            return false;
        }
        int row = 0;
        int col = matrix[0].length - 1;

        while (row < matrix.length && col >= 0) {
            int current = matrix[row][col];

            if (current > target) {
                col--;
            } else if (current < target) {
                row++;
            } else {
                return true;
            }
        }

        return false;
    }
	```
- 提交结果
	- Runtime: 5 ms, faster than 100.00% of Java online submissions for Search a 2D Matrix II.
	- Memory Usage: 42.1 MB, less than 100.00% of Java online submissions for Search a 2D Matrix II. 
