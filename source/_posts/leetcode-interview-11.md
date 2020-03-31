---
title: LeetCode.面试题11-旋转数组的最小数字
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-03-31 11:23:41
---
###### Question
- Source
	- [面试题11. 旋转数组的最小数字](https://leetcode-cn.com/problems/xuan-zhuan-shu-zu-de-zui-xiao-shu-zi-lcof/) 
- Title
	- 面试题11. 旋转数组的最小数字 
- Content
	- 把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。输入一个递增排序的数组的一个旋转，输出旋转数组的最小元素。例如，数组 [3,4,5,1,2] 为 [1,2,3,4,5] 的一个旋转，该数组的最小值为1。 
<!--more-->

###### Answer
- 思路
	- 递增数组的旋转，所以遍历数组，如果前一个元素比后一个元素大，则后一个元素就是最小的元素。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int minArray(int[] numbers) {
        int pos = 0;
        for(int i = 1 ; i < numbers.length;i++){
            if(numbers[i-1] > numbers[i]){
                pos = i;
                break;
            }
        }
        return numbers[pos];
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :39.7 MB, 在所有 Java 提交中击败了100.00%的用户
