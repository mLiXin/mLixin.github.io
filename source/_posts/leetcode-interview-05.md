---
title: LeetCode.面试题05-替换空格
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-03-30 18:02:26
---
###### Question
- Source
	- [面试题05. 替换空格](https://leetcode-cn.com/problems/ti-huan-kong-ge-lcof/) 
- Title
	- 面试题05. 替换空格 
- Content
	- 请实现一个函数，把字符串 s 中的每个空格替换成"%20"。 
<!--more-->

###### Answer
- 思路
	- StringBuilder解决，遍历字符串，如果是空格则append'%20'，否则直接append(s.charAt(i));
	- 如果从字符串数组方面去考虑的话，可以先遍历数出来空格数一共有多少，然后新建`空格数*2+s.length`长度的数组，从后往前依次填充字符串数组即可
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public String replaceSpace(String s) {
        StringBuilder sb = new StringBuilder();
        for(int i = 0;i<s.length();i++){
            if(s.charAt(i) == ' '){
                sb.append("%20");
            }else{
                sb.append(s.charAt(i));
            }
        }
        return sb.toString();
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :37.4 MB, 在所有 Java 提交中击败了100.00%的用户 
