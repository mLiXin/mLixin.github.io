---
title: LeetCode.09-Palindrome Number
date: 2019-07-15 18:18:59
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
	- [9.Palindrome Number](https://leetcode.com/problems/palindrome-number/)
- Title
	- Palindrome Number
- Content 
	- Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.
<!--more-->

###### Answer
- 思路
    - 计算x后半部分反转的reverseX的值，然后比较两个值就可以了。
- 时间复杂度
    - O(n)
- 空间复杂度
    - O(1)
- 代码实现
    
    ```
    public boolean isPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) {
            return false;
        } else {
            int reverseX = 0;
            while (x > reverseX) {
                reverseX = reverseX * 10 + x % 10;
                x = x / 10;
            }

            return x == reverseX || reverseX / 10 == x;
        }
    }
    ```
    
- 提交结果
   - Runtime: 6 ms, faster than 100.00% of Java online submissions for Palindrome Number.
	- Memory Usage: 35.5 MB, less than 11.05% of Java online submissions for Palindrome Number.
