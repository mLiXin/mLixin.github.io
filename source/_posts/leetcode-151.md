---
title: LeetCode.151-翻转字符串里的单词
date: 2020-04-10 10:20:38
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
	- [151. 翻转字符串里的单词](https://leetcode-cn.com/problems/reverse-words-in-a-string/) 
- Title
	- 151. 翻转字符串里的单词 
- Content
	- 给定一个字符串，逐个翻转字符串中的每个单词。
<!--more-->

###### Answer
- 思路
	- 四个步骤：去除首尾空格、以空格分为String数组、reverseString数据、拼接字符串。 
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public String reverseWords(String s) {
        String[] resultArray = s.trim().split(" ");
        StringBuilder sb = new StringBuilder();
        for(int i = resultArray.length -1 ;i>=0;i--){
            if(!resultArray[i].isEmpty()){
                sb.append(resultArray[i]+" ");
            }
        }
        
        return sb.toString().trim();
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :40.1 MB, 在所有 Java 提交中击败了5.48%的用户
