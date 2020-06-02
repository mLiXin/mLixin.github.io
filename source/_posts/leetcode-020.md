---
title: LeetCodee.020-Valid Parentheses
date: 2019-09-10 10:08:09
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
	- [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) 
- Title
	- Valid Parentheses 	
- Content 
	- Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. 
<!--more-->

###### Answer
- 思路
	- 利用栈实现
	- 直接用数组实现类似栈的结构，存取更快
- 时间复杂度
	- O(n) 
- 代码实现

	```Java
	public boolean isValid(String s) {
        if (s.length() % 2 != 0) {
            return false;
        }

        char[] arrayStack = new char[s.length()];
        int currentTopPos = 0;
        for (int i = 0; i < s.length(); i++) {
            char current = s.charAt(i);
            switch (current) {
                case '(':
                case '{':
                case '[':
                    arrayStack[currentTopPos] = current;
                    currentTopPos++;
                    break;
                case ')':
                    if (currentTopPos != 0 && arrayStack[currentTopPos - 1] == '(') {
                        arrayStack[currentTopPos - 1] = '#';
                        currentTopPos--;
                    } else {
                        return false;
                    }
                    break;
                case '}':
                    if (currentTopPos != 0 && arrayStack[currentTopPos - 1] == '{') {
                        arrayStack[currentTopPos - 1] = '#';
                        currentTopPos--;
                    } else {
                        return false;
                    }
                    break;
                case ']':
                    if (currentTopPos != 0 && arrayStack[currentTopPos - 1] == '[') {
                        arrayStack[currentTopPos - 1] = '#';
                        currentTopPos--;
                    } else {
                        return false;
                    }
                    break;
            }
        }
        return currentTopPos == 0;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Valid Parentheses.
	- Memory Usage: 34.2 MB, less than 100.00% of Java online submissions for Valid Parentheses. 

