---
title: LeetCode.066-Plus One
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories: LeetCode
visible: hide
date: 2019-09-16 09:56:52
---
###### Question
- Source
	- [66. Plus One](https://leetcode.com/problems/plus-one/) 
- Title
	- Plus One 
- Content
	- Given a non-empty array of digits representing a non-negative integer, plus one to the integer.The digits are stored such that the most significant digit is at the head of the list, and each element in the array contain a single digit.You may assume the integer does not contain any leading zero, except the number 0 itself.
<!--more-->

###### Answer
- 思路
	- 从低位往高位计算即可，注意99这种的情况
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int[] plusOne(int[] digits) {
        int carry = 1;
        int currentPos = digits.length -1;
        while(carry == 1 && currentPos >=0){
            int currentSum = carry + digits[currentPos];
            if(currentSum >9){
                digits[currentPos--] = currentSum -10;
                carry = 1;
            }else{
                digits[currentPos--] = currentSum;
                carry = 0;
            }
        }
        
        if(carry == 1){
            int[] result = new int[digits.length+1];
            result[0] = carry;
            for(int i = 1;i<result.length;i++){
                result[i] = digits[i-1];
            }
            return result;
        }else{
            return digits;    
        }
        

    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Plus One.
	- Memory Usage: 35.1 MB, less than 97.58% of Java online submissions for Plus One.
