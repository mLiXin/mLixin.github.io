---
title: LeetCode.038-Count and Say
date: 2019-09-12 10:22:37
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
	- [38. Count and Say](https://leetcode.com/problems/count-and-say/) 
- Title
	- Count and Say
- Content
	- The count-and-say sequence is the sequence of integers with the first five terms as following:
	
	```
	1.     1
	2.     11
	3.     21
	4.     1211
	5.     111221
	```
1 is read off as "one 1" or 11.
11 is read off as "two 1s" or 21.
21 is read off as "one 2, then one 1" or 1211.

	Given an integer n where 1 ≤ n ≤ 30, generate the nth term of the count-and-say sequence.
<!--more-->

###### Answer
- 思路
	- 思路1递归，拿到n-1的字符串，直接数这个字符串即可
	- 思路2数组，从1开始遍历，一直到n，每个n对应的字符串用数组存储，每次取下标为n-1的字符串去数即可。用数组的话，空间复杂度会大一些。
- 时间复杂度
	- O(n2)? 	
- 代码实现

	```Java
	public String countAndSay(int n) {
        if (n < 1) {
            return "";
        }

        if (n == 1) {
            return "1";
        }

        String pre = countAndSay(n - 1);

        StringBuilder result = new StringBuilder();
        System.out.println(pre);
        int currentCount = 1;
        char currentChar = pre.charAt(0);
        for (int i = 1; i < pre.length(); i++) {
            char current = pre.charAt(i);
            if (currentChar != current) {
                result.append(currentCount).append(currentChar);

                currentChar = current;
                currentCount = 1;
            } else {
                currentCount++;
            }
        }

        result.append(currentCount).append(currentChar);

        return result.toString();
    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 99.42% of Java online submissions for Count and Say.
	- Memory Usage: 34 MB, less than 100.00% of Java online submissions for Count and Say.
