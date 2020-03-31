---
title: LeetCode.面试题04-二维数组中的查找
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-03-30 16:31:40
---
###### Question
- Source
	- [面试题04. 二维数组中的查找](https://leetcode-cn.com/problems/er-wei-shu-zu-zhong-de-cha-zhao-lcof/) 
- Title
	- 面试题04. 二维数组中的查找 
- Content
	- 在一个 n * m 的二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。
<!--more-->

###### Answer
- 思路
	- 通过题目可以看出来，二维矩阵的右上角的数字，属于该行最大， 该列最小，那就以这个值来和target对比，如果target大于该值，则target肯定不在该值的行中；如果小于该值，则target肯定不在该值所在的列中。
- 时间复杂度
	- O(n+m) 	
- 代码实现

	```Java
	public boolean findNumberIn2DArray(int[][] matrix, int target) {

        if(matrix == null || matrix.length == 0){
            return false;
        }
        int startRow = 0;
        int endRow = matrix.length-1;
        int startCol = 0;
        int endCol = matrix[0].length-1;

        while (startRow <= endRow && startCol <= endCol){
            if(target < matrix[startRow][endCol]){
                endCol --;
            }else if(target > matrix[startRow][endCol]){
                startRow ++;
            }else{
                return true;
            }
        }
        return false;
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :48.6 MB, 在所有 Java 提交中击败了100.00%的用户
