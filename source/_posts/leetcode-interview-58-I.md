---
title: LeetCode.面试题58-I-翻转单词顺序
date: 2020-04-15 14:07:45
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
	- [面试题58 - I. 翻转单词顺序](https://leetcode-cn.com/problems/fan-zhuan-dan-ci-shun-xu-lcof/) 
- Title
	- 面试题58 - I. 翻转单词顺序 
- Content
	- 输入一个英文句子，翻转句子中单词的顺序，但单词内字符的顺序不变。为简单起见，标点符号和普通字母一样处理。例如输入字符串"I am a student. "，则输出"student. a am I"。

<!--more-->

###### Answer
- 思路
	- 根据空格对String分组，反向append即可 
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public String reverseWords(String s) {
        String[] array = s.split(" ");
        StringBuilder resultStr = new StringBuilder();
        for(int i = array.length-1;i>=0;i--){
            if(array[i].isEmpty()){
                continue;
            }

            if(i != array.length-1){
                resultStr.append(" ");
            }
            resultStr.append(array[i]);
        }
        return resultStr.toString();
    }
	```
- 提交结果
	- 执行用时 :2 ms, 在所有 Java 提交中击败了95.07%的用户
	- 内存消耗 :39.6 MB, 在所有 Java 提交中击败了100.00%的用户
