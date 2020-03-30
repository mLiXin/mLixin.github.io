---
title: LeetCode.071-Simplify Path
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories:
  - LeetCode
date: 2019-11-26 11:14:11
---
###### Question
- Source
	- [71. Simplify Path](https://leetcode.com/problems/simplify-path/) 
- Title
	- 71. Simplify Path 
- Content
	- Given an absolute path for a file (Unix-style), simplify it. Or in other words, convert it to the canonical path.
	- In a UNIX-style file system, a period . refers to the current directory. Furthermore, a double period .. moves the directory up a level. For more information, see: Absolute path vs relative path in Linux/Unix
	- Note that the returned canonical path must always begin with a slash /, and there must be only a single slash / between two directory names. The last directory name (if it exists) must not end with a trailing /. Also, the canonical path must be the shortest string representing the absolute path. 
<!--more-->

###### Answer
- 思路
	- 类似栈实现，每次记录字符串，遇到`/`的时候处理，如果是`..`则出栈，`.`不用管，其他的都可以看做目录
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	class Solution {
       public String simplifyPath(String path) {

        char[] chars = path.toCharArray();

        StringBuilder tempBuilder = new StringBuilder();
        String[] stack = new String[chars.length];
        int stackIndex = 0;
        for (int i = 0; i < chars.length; i++) {
            char cur = chars[i];

            switch (cur) {
                case '/':
                    while (i + 1 < chars.length && chars[i + 1] == '/') {
                        i++;
                    }

                    if (tempBuilder.toString().equals(".")) {

                    } else if (tempBuilder.toString().equals("..")) {
                        if (stackIndex > 0) {
                            stackIndex--;
                        }
                    } else {
                        if (tempBuilder.length() > 0) {
                            stack[stackIndex++] = tempBuilder.toString();
                        }
                    }

                    tempBuilder = new StringBuilder();
                    break;
                default:
                    tempBuilder.append(cur);
                    break;
            }
        }
        if (tempBuilder.toString().equals(".")) {

        } else if (tempBuilder.toString().equals("..")) {
            if (stackIndex > 0) {
                stackIndex--;
            }
        } else {
            if (tempBuilder.length() > 0) {
                stack[stackIndex++] = tempBuilder.toString();
            }
        }

        if (stackIndex == 0) {
            return "/";
        }
        
        StringBuilder resultBuilder = new StringBuilder();

        for (int i = 0; i < stackIndex; i++) {
            resultBuilder.append("/");
            resultBuilder.append(stack[i]);
        }

        return resultBuilder.toString();
    	}
	}
	```
- 提交结果
	- Runtime: 2 ms, faster than 99.80% of Java online submissions for Simplify Path.
	- Memory Usage: 38.1 MB, less than 80.00% of Java online submissions for Simplify Path. 
