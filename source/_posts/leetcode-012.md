---
title: LeetCode.012-Integer to Roman
date: 2019-07-24 17:44:46
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
	- [12. Integer to Roman](https://leetcode.com/problems/integer-to-roman/)
- Title
	- Integer to Roman
- Content 
	- Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.
<!--more-->

###### Answer
- 思路
    - 从大数往小数去计算，中间多900 to "CM"、400 to "CD"、90 to "XC"、40 to "XL、9 to "IX、4 to "IV"，
- 时间复杂度
    - O(n)
- 空间复杂度
    - O(1)
- 代码实现

    ```Java
    public String intToRoman(int num) {

        StringBuilder builder = new StringBuilder();

        int[] numArray = { 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1 };
        String[] strArray = { "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I" };

        for (int i = 0; i < numArray.length && num > 0; i++) {

            while (num >= numArray[i]) {
                builder.append(strArray[i]);
                num -= numArray[i];
            }
        }

        return builder.toString();
    }
    ```
- 提交结果
   - Runtime: 3 ms, faster than 100.00% of Java online submissions for Integer to Roman.
	- Memory Usage: 36.1 MB, less than 100.00% of Java online submissions for Integer to Roman.
