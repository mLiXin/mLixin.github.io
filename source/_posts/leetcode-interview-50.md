---
title: LeetCode.面试题50-第一个只出现一次的字符
date: 2020-04-14 10:21:12
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
	- [面试题50. 第一个只出现一次的字符]() 
- Title
	- 面试题50. 第一个只出现一次的字符 
- Content
	- 在字符串 s 中找出第一个只出现一次的字符。如果没有，返回一个单空格。
<!--more-->

###### Answer
- 思路
	- 创建一个int[256]用来存放每个字符的个数，下标为字符的ASCII码值，然后从前遍历字符串，返回第一个count为1的字符 
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public char firstUniqChar(String s) {
        char[] array = s.toCharArray();

        int[] countArray = new int[256];

        for(int i = 0; i < array.length;i++){
            countArray[array[i]]++;
        }

        for(int i = 0;i< array.length;i++){
            if(countArray[array[i]] == 1){
                return array[i];
            }
        }

        return ' ';
    }
	```
- 提交结果
	- 执行用时 :4 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :40.5 MB, 在所有 Java 提交中击败了100.00%的用户
