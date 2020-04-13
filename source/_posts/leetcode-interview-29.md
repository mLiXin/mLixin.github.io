---
title: LeetCode.面试题29-顺时针打印矩阵
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-04-13 10:03:46
---
###### Question
- Source
	- [面试题29. 顺时针打印矩阵](https://leetcode-cn.com/problems/shun-shi-zhen-da-yin-ju-zhen-lcof/) 
- Title
	- 面试题29. 顺时针打印矩阵 
- Content
	- 输入一个矩阵，按照从外向里以顺时针的顺序依次打印出每一个数字。 
<!--more-->

###### Answer
- 思路
	- 模拟打印过程就可以了。每次打印的时候都看成列数从left到right，行数从top到bottom：
		- 左上到右上打印即row为top，column从left到right，打印完毕，top++；
		- 右上到右下打印即col为right，row从top到bottom，right--；
		- 右下到左下打印即row为bottom，col从right到left，bottom--；
		- 左下到左上打印即col为left，row从bottom到top，left--。
- 时间复杂度
	- O(m*n) 	
- 代码实现

	```Java
	public int[] spiralOrder(int[][] matrix) {
        if (matrix.length == 0) {
            return new int[0];
        }
        int top = 0, bottom = matrix.length - 1, left = 0, right = matrix[0].length - 1;
        int[] res = new int[(bottom + 1) * (right + 1)];
        int pos = 0;
        while (true) {
            // 左上到右上
            for (int i = left; i <= right; i++) {
                res[pos++] = matrix[top][i];
            }

            if ( ++top > bottom) {
                break;
            }
            
            // 右上到右下
            for (int i = top; i <= bottom; i++) {
                res[pos++] = matrix[i][right];
            }
            if (--right < left) {
                break;
            }
            
            // 右下到左下
            for (int i = right; i >= left; i--) {
                res[pos++] = matrix[bottom][i];
            }
            if (--bottom < top) {
                break;
            }
            
            // 左下到左上
            for (int i = bottom; i >= top; i--) {
                res[pos++] = matrix[i][left];
            }
            if (++left > right) {
                break;
            }
        }
        return res;
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了97.31%的用户
	- 内存消耗 :41 MB, 在所有 Java 提交中击败了100.00%的用户
