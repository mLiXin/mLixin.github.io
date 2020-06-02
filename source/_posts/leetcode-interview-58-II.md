---
title: LeetCode.面试题58-II-左旋转字符串
date: 2020-04-15 14:16:01
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
	- [面试题58 - II. 左旋转字符串](https://leetcode-cn.com/problems/zuo-xuan-zhuan-zi-fu-chuan-lcof/) 
- Title
	- 面试题58 - II. 左旋转字符串 
- Content
	- 字符串的左旋转操作是把字符串前面的若干个字符转移到字符串的尾部。请定义一个函数实现字符串左旋转操作的功能。比如，输入字符串"abcdefg"和数字2，该函数将返回左旋转两位得到的结果"cdefgab"。
<!--more-->

###### Answer
- 思路
	- 反转数组
	- 拼接字符串
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	// 反转数组
	public String reverseLeftWords(String s, int n) {
        char[] array = s.toCharArray();

        reverse(array,0,array.length-1);
        reverse(array,0,array.length - n-1);
        reverse(array,array.length-n,array.length-1);

        return new String(array);
    }

    public void reverse(char[] array,int left,int right){
        while(left < right){
            char temp = array[left];
            array[left] = array[right];
            array[right] = temp;

            left ++;
            right --;
        }
    }
    
    // 拼接字符串
    
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :39.6 MB, 在所有 Java 提交中击败了100.00%的用户
