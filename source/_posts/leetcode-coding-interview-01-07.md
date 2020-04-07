---
title: LeetCode.面试题01.07-旋转矩阵
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories:
  - LeetCode
date: 2020-04-07 10:39:17
---
###### Question
- Source
	- [面试题 01.07. 旋转矩阵](https://leetcode-cn.com/problems/rotate-matrix-lcci/) 
- Title
	- 面试题 01.07. 旋转矩阵 
- Content
	- 给你一幅由 N × N 矩阵表示的图像，其中每个像素的大小为 4 字节。请你设计一种算法，将图像旋转 90 度。
<!--more-->

###### Answer
- 思路
	- 对角swap+左右swap即可，不占用额外内存
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	public void rotate(int[][] matrix) {
        if(matrix == null || matrix.length == 0){
            return;
        }
        int maxRow = matrix.length-1;
        int maxCol = matrix[0].length-1;
        // 对角swap
        for(int i = 0;i<=maxRow;i++){
            for(int j = i+1;j<=maxCol;j++){
                swap(matrix,i,j,j,i);
            }
        }
        // 左右swap
        for(int i = 0;i<= maxRow;i++){
            for(int j = 0;j<= maxCol / 2;j++){
                swap(matrix,i,j,i,maxCol - j);
            }
        }
    }

    public void swap(int[][] array,int i,int j,int desI,int desJ){
        int temp = array[i][j];
        array[i][j] = array[desI][desJ];
        array[desI][desJ] = temp;
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :39.5 MB, 在所有 Java 提交中击败了100.00%的用户
