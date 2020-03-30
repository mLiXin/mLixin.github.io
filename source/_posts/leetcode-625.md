---
title: LeetCode.625-最小因式分解
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories: LeetCode
visible: hide
date: 2019-10-11 17:40:33
---
###### Question
- Source
	- [](https://leetcode-cn.com/problems/minimum-factorization/submissions/) 
- Title
	- 625. 最小因式分解 
- Content
	- 给定一个正整数 a，找出最小的正整数 b 使得 b 的所有数位相乘恰好等于 a。如果不存在这样的结果或者结果不是 32 位有符号整数，返回 0。
<!--more-->

###### Answer
- 思路
	- 从9往2开始去整除，用stringBuilder记录下来。
- 时间复杂度
	- O(1) 	
- 代码实现

	```Java
	public int smallestFactorization(int a) {

        if (a < 10){
            return a;
        }

        StringBuilder resultBuilder = new StringBuilder();

        int current = 9;
        while (a >= 10 && current > 1) {

            if (a % current == 0) {
                resultBuilder.append(current);
                a = a / current;
                continue;
            }

            current--;
        }

        if (a >= 10) {
            return 0;
        }

        resultBuilder.append(a);

        long result = 0;

        for (int i = resultBuilder.length() - 1; i >= 0; i--) {
            result = result * 10 + (resultBuilder.charAt(i) - '0');
            if (result > Integer.MAX_VALUE) {
                return 0;
            }
        }
        return (int) result;
    }
	```
- 提交结果
	- 执行用时:1ms，在所有Java提交中击败了95.24%的用户
	- 内存消耗:33.4MB，在所有Java提交中击败了100.00%的用户 
