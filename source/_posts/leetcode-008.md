---
title: LeetCode.008-String to Integer
date: 2019-07-15 11:21:30
tags:
- LeetCode
- Algorithm
- Java
- LeetCode-Medium
categories: LeetCode
visible: hide
---
###### Question
- Source
	- [8.String to Integer](https://leetcode.com/problems/string-to-integer-atoi/)
- Title
	-  String to Integer 
- Content 
	- Implement atoi which converts a string to an integer.The function first discards as many whitespace characters as necessary until the first non-whitespace character is found. Then, starting from this character, takes an optional initial plus or minus sign followed by as many numerical digits as possible, and interprets them as a numerical value.The string can contain additional characters after those that form the integral number, which are ignored and have no effect on the behavior of this function.If the first sequence of non-whitespace characters in str is not a valid integral number, or if no such sequence exists because either str is empty or it contains only whitespace characters, no conversion is performed.If no valid conversion could be performed, a zero value is returned.
<!--more-->

###### Answer
- 思路
    - 先处理字符串，将符合要求的字符串截取下来
    - 再将处理过后的字符串转为整型
- 时间复杂度
    - O(n)
- 空间复杂度
    - O(1)
- 代码实现
    
    ```
    public int myAtoi(String str) {

        StringBuilder resultStr = new StringBuilder();
        // 先处理字符串，符合要求的留下
        for (int i = 0; i < str.length(); i++) {
            char current = str.charAt(i);
            switch (current) {
                case ' ':
                    if (resultStr.length() > 0) {
                        i = str.length();
                    }
                    break;
                case '+':
                case '-':
                    if (resultStr.length() == 0) {
                        resultStr.append(current);
                    } else {
                        i = str.length();
                    }
                    break;
                case '0':
                case '1':
                case '2':
                case '3':
                case '4':
                case '5':
                case '6':
                case '7':
                case '8':
                case '9':
                    resultStr.append(current);
                    break;
                default:
                    i = str.length();
                    break;
            }

        }

        long result = 0;
        boolean flag_negative = false;
        for (int i = 0; i < resultStr.length(); i++) {
            char current = resultStr.charAt(i);
            switch (current) {
                case '+':
                    flag_negative = false;
                    break;
                case '-':
                    flag_negative = true;
                    break;
                default:
                    result = result * 10 + current - '0';
                    break;
            }

            if (flag_negative) {
                if (-1 * result < Integer.MIN_VALUE) {
                    return Integer.MIN_VALUE;
                }
            } else {
                if (result > Integer.MAX_VALUE) {
                    return Integer.MAX_VALUE;
                }
            }
        }

        if (flag_negative) {
            result = result * -1;
        }

        return (int) result;
    }
    ```
- 提交结果
    -  Runtime: 1 ms, faster than 100.00% of Java online submissions for String to Integer (atoi).
	- Memory Usage: 36.1 MB, less than 99.92% of Java online submissions for String to Integer (atoi).