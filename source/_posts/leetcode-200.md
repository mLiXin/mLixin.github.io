---
title: LeetCode.200-Number of Islands
date: 2019-09-24 13:44:25
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
	- [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) 
- Title
	- 200. Number of Islands 
- Content
	- Given a 2d grid map of '1's (land) and '0's (water), count the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.
<!--more-->

###### Answer
- 思路
	- 深度优先遍历，将相连接的'1'置为'0'
- 时间复杂度
	- O(m * n) 	
- 代码实现

	```Java
	public int numIslands(char[][] grid) {

        int num = 0;
        for (int i = 0; i < grid.length; i++) {

            for (int j = 0; j < grid[i].length; j++) {
                if (grid[i][j] == '1') {
                    dfs(grid, i, j);
                    num++;
                }
            }
        }
        return num;
    }

    public void dfs(char[][] grid, int targetRow, int targetCol) {
        if (targetRow >= grid.length || targetRow < 0
                || targetCol >= grid[targetRow].length || targetCol < 0
                || grid[targetRow][targetCol] == '0') {
            return;
        }

        grid[targetRow][targetCol] = '0';

        // 向上
        dfs(grid, targetRow - 1, targetCol);

        // 向右
        dfs(grid, targetRow, targetCol + 1);

        // 向下
        dfs(grid, targetRow + 1, targetCol);

        // 向左
        dfs(grid, targetRow, targetCol - 1);

    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 100.00% of Java online submissions for Number of Islands.
	- Memory Usage: 40.9 MB, less than 90.70% of Java online submissions for Number of Islands.
