---
title: LeetCode.面试题17-打印从1到最大的n位数
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-04-08 10:14:24
---
###### Question
- Source
	- [面试题17. 打印从1到最大的n位数](https://leetcode-cn.com/problems/da-yin-cong-1dao-zui-da-de-nwei-shu-lcof/) 
- Title
	- 面试题17. 打印从1到最大的n位数 
- Content
	- 输入数字 n，按顺序打印出从 1 到最大的 n 位十进制数。比如输入 3，则打印出 1、2、3 一直到最大的 3 位数 999。
<!--more-->

###### Answer
- 思路
	- 根据n获取最大数字，依次打印即可。
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	public int[] printNumbers(int n) {
        int maxNum = 0;
        while(n > 0){
            maxNum = maxNum*10+9;
            n--;
        }
        int[] result = new int[maxNum];
        for(int i = 0 ; i < result.length;i++){
            result[i] = i+1;
        }
        return result;
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :47.1 MB, 在所有 Java 提交中击败了100.00%的用户
