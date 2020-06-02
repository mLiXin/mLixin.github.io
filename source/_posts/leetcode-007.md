---
title: LeetCode.007-Reverse Integer
date: 2019-07-15 09:50:25
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
	- [7.Reverse Integer](https://leetcode.com/problems/reverse-integer/)
- Title
	- Reverse Integer
- Content 
	- Given a 32-bit signed integer, reverse digits of an integer.
<!--more-->

###### Answer
- 思路
	- 每次将x除以10拿到小数位，然后添加到result的小数位上。
- 时间复杂度
	- O(n) n为整数位数
- 空间复杂度
	- O(n)
- 代码实现

	```
	public int reverse(int x) {

        long result = 0;

        while (x / 10 != 0) {
            result = result * 10 + x % 10;
            x = x / 10;
        }

        if (x != 0) {
            result = result * 10 + x % 10;
        }

        if (result > Integer.MAX_VALUE || result < Integer.MIN_VALUE) {
            return 0;
        }

        return (int) result;
    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 100.00% of Java online submissions for Reverse Integer.
	- Memory Usage: 33.5 MB, less than 7.60% of Java online submissions for Reverse Integer.