---
title: LeetCode.064-Minimum Path Sum
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories:
  - LeetCode
date: 2019-10-31 09:59:37
---
###### Question
- Source
	- [64. Minimum Path Sum]() 
- Title
	- 64. Minimum Path Sum 
- Content
	- Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right which minimizes the sum of all numbers along its path.
<!--more-->

###### Answer
- 思路
	- 动态规划，创建临时二维数组，大小和grid一致，里面存放从左上角到该位置的最小路径和，即该位置+Math.min(左边数值，上边数值)
- 时间复杂度
	- O(m*n) 	
- 代码实现

	```Java
	public int minPathSum(int[][] grid) {
        if (grid == null || grid.length == 0) {
            return 0;
        }

        int m = grid.length;
        int n = grid[0].length;

        int[][] temp = new int[m][n];
        temp[0][0] = grid[0][0];

        for (int i = 1; i < n; i++) {
            temp[0][i] = temp[0][i - 1] + grid[0][i];
        }

        for (int i = 1; i < m; i++) {
            temp[i][0] = temp[i - 1][0] + grid[i][0];
        }

        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                temp[i][j] = Math.min(temp[i - 1][j], temp[i][j - 1]) + grid[i][j];
            }
        }

        return temp[m - 1][n - 1];
    }
	```
- 提交结果
	- Runtime: 2 ms, faster than 90.15% of Java online submissions for Minimum Path Sum.
	- Memory Usage: 42 MB, less than 87.84% of Java online submissions for Minimum Path Sum.
