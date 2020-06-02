---
title: LeetCode.006-ZigZag Conversion
date: 2019-07-12 16:36:29
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
	- [6.ZigZag Conversion](https://leetcode.com/problems/zigzag-conversion/)
- Title
	- ZigZag Conversion
- Content 
	- The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)
	
		```
		P   A   H   N
		A P L S I I G
		Y   I   R
		```
	And then read line by line: "PAHNAPLSIIGYIR"
Write the code that will take a string and make this conversion given a number of rows:string convert(string s, int numRows);
<!--more-->

###### Answer
- 思路
	- 分析，可以以一个`|/`为分隔单位，这个分割单位一共有2 * (numRows - 1)个元素，其中`|`从上往下走，`/`从下往上走；
	- 新建一个临时字符数组，遍历字符串，将字符串中每个字符找机会放到临时字符数组的对应位置上。
	- 对于一个分隔单位来说，第一行和最后一行只有一个元素，中间行都有两个元素，一个是i，另一个是count-i。
- 时间复杂度
	- O(n) 
- 空间复杂度
	- O(n) 
- 代码实现

	```
	public String convert(String s, int numRows) {

        if (s.length() < numRows || numRows == 1) {
            return s;
        }

        int countIndex = 2 * (numRows - 1);
        int length = s.length();

        char[] array = new char[length];
        int arrayIndex = 0;
        for (int i = 0; i < numRows; i++) {

            for (int j = i; j < length; j = j + countIndex) {

                array[arrayIndex++] = s.charAt(j);

                if (i > 0 && i < numRows - 1 && (j + countIndex - 2 * i) < length) {

                    array[arrayIndex++] = s.charAt(j + countIndex - 2 * i);
                }
            }
        }

        return new String(array);
    }
	```
- 提交结果
	- Runtime: 2 ms, faster than 100.00% of Java online submissions for ZigZag Conversion.
	- Memory Usage: 36.5 MB, less than 99.73% of Java online submissions for ZigZag Conversion. 