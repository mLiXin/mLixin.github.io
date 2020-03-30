---
title: LeetCode.013-Roman to Integer
date: 2019-08-08 13:42:14
tags:
- LeetCode
- Algorithm
- Java
- LeetCode-Easy
categories: LeetCode
visible: hide
---
###### Question
- Source
	- [13. Roman to Integer](https://leetcode.com/problems/roman-to-integer/)
- Title
	- Roman to Integer
- Content 
	- Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.
<!--more-->

###### Answer
- 思路
    - 观察可知道，罗马数字中，如果前一个字符比后一个字符代表的数字小，说明是减，其他情况是加。
- 时间复杂度
    - O(n)
- 空间复杂度
    - O(1)
- 代码实现

    ```Java
    public int romanToInt(String s) {

        int nextValue = Integer.MIN_VALUE;
        int result = 0;

        for (int i = s.length() - 1; i >= 0; i--) {
            int currentValue = nextValue;
            switch (s.charAt(i)) {
                case 'I':
                    currentValue = 1;
                    break;
                case 'V':
                    currentValue = 5;
                    break;
                case 'X':
                    currentValue = 10;
                    break;
                case 'L':
                    currentValue = 50;
                    break;
                case 'C':
                    currentValue = 100;
                    break;
                case 'D':
                    currentValue = 500;
                    break;
                case 'M':
                    currentValue = 1000;
                    break;
            }

            if (currentValue < nextValue) {
                result -= currentValue;
            } else {
                result += currentValue;
            }
            nextValue = currentValue;
        }
        return result;
    }
    
    ```
- 提交结果
	- Runtime: 3 ms, faster than 100.00% of Java online submissions for Roman to Integer.
	- Memory Usage: 36.3 MB, less than 100.00% of Java online submissions for Roman to Integer.
