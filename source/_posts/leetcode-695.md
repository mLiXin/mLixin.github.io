---
title: LeetCode.695-Max Area of Island
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories:
  - LeetCode
date: 2019-11-20 10:58:51
---
###### Question
- Source
	- [695. Max Area of Island]() 
- Title
	- 695. Max Area of Island 
- Content
	- Given a non-empty 2D array grid of 0's and 1's, an island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.
	- Find the maximum area of an island in the given 2D array. (If there is no island, the maximum area is 0.) 
<!--more-->

###### Answer
- 思路
	- 广度优先遍历，并将访问过的1置为0
- 时间复杂度
	- O(m*n) 	
- 代码实现

	```Java
	public int maxAreaOfIsland(int[][] grid) {
        if (grid == null || grid.length == 0) {
            return 0;
        }

        int maxSum = 0;
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {

                if (grid[i][j] == 1) {
                    int currentSum = bfs(grid, i, j);
                    maxSum = Math.max(currentSum, maxSum);
                }
            }
        }

        return maxSum;
    }

    public int bfs(int[][] grid, int i, int j) {

        if (i < 0 || i >= grid.length || j < 0 || j >= grid[i].length) {
            return 0;
        }
        if (grid[i][j] != 1) {
            return 0;
        }

        int sum = 1;
        grid[i][j] = 0;

        // 上
        sum += bfs(grid, i - 1, j);

        // 右
        sum += bfs(grid, i, j + 1);

        // 下
        sum += bfs(grid, i + 1, j);

        // 左
        sum += bfs(grid, i, j - 1);
        return sum;
    }
	```
- 提交结果
	- Runtime: 2 ms, faster than 99.74% of Java online submissions for Max Area of Island.
	- Memory Usage: 43.9 MB, less than 55.56% of Java online submissions for Max Area of Island. 
