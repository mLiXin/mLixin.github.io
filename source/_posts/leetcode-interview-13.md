---
title: LeetCode.面试题13-机器人的运动范围
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories:
  - LeetCode
date: 2020-04-08 10:04:42
---
###### Question
- Source
	- [面试题13. 机器人的运动范围](https://leetcode-cn.com/problems/ji-qi-ren-de-yun-dong-fan-wei-lcof/) 
- Title
	- 面试题13. 机器人的运动范围 
- Content
	- 地上有一个m行n列的方格，从坐标 [0,0] 到坐标 [m-1,n-1] 。一个机器人从坐标 [0, 0] 的格子开始移动，它每次可以向左、右、上、下移动一格（不能移动到方格外），也不能进入行坐标和列坐标的数位之和大于k的格子。例如，当k为18时，机器人能够进入方格 [35, 37] ，因为3+5+3+7=18。但它不能进入方格 [35, 38]，因为3+5+3+8=19。请问该机器人能够到达多少个格子？

<!--more-->

###### Answer
- 思路
	- 分析题意可知，二维数组中分为可达解、不可达解、非解。从{0,0}开始深度或广度遍历即可。
- 时间复杂度
	- O(m*n) 	
- 代码实现

	```Java
	int[] tempSum;
    int count = 0;
    boolean[][] visited;
    public int movingCount(int m, int n, int k) {
        tempSum = new int[Math.max(m,n)];
        visited = new boolean[m][n];
        canCurrentArrive(0,0,k,m,n);
        return count;
    }

    public void canCurrentArrive(int i,int j,int k,int m,int n){
        if(i>=m || j >=n || visited[i][j]){
            return;
        }
        visited[i][j] = true;
        if(getSum(i) + getSum(j) <= k){
            count++;
            canCurrentArrive(i+1,j,k,m,n);
            canCurrentArrive(i,j+1,k,m,n);
        }
    }

    public int getSum(int number){
        if(number < 10){
            tempSum[number] = number;
            return number;
        }

        if(tempSum[number] != 0){
            return tempSum[number];
        }
        int sum = 0;
        while(number > 0){
            sum += number % 10;
            number /= 10;
        }
        tempSum[number] = sum;
        return sum;
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了90.38%的用户
	- 内存消耗 :36 MB, 在所有 Java 提交中击败了100.00%的用户
