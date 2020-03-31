---
title: LeetCode.面试题06-从尾到头打印链表
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-xxx
categories:
  - LeetCode
date: 2020-03-30 18:09:29
---
###### Question
- Source
	- [面试题06. 从尾到头打印链表](https://leetcode-cn.com/problems/cong-wei-dao-tou-da-yin-lian-biao-lcof/) 
- Title
	- 面试题06. 从尾到头打印链表 
- Content
	- 输入一个链表的头节点，从尾到头反过来返回每个节点的值（用数组返回）。
<!--more-->

###### Answer
- 思路
	- 从数组角度来说，直接遍历获取到链表的长度，创建数组，从头往后遍历链表，从后往前填充数组即可
	- 另外一种思路则是反转链表，不过题目要求的是返回数组，反转链表一样要计算链表的长度然后创建数组，就没啥必要了。
	- 题解里还有什么借助栈什么的，但是直接从后往前填充数组不香吗？
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int[] reversePrint(ListNode head) {
        int arrayCount = 0;
        ListNode temp = head;
        while (temp != null){
            arrayCount++;
            temp = temp.next;
        }
        
        int[] array = new int[arrayCount];
        int pos = arrayCount-1;
        while (head != null){
            array[pos--] = head.val;
            head = head.next;
        }
        
        return array;
    }
    
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :39.6 MB, 在所有 Java 提交中击败了100.00%的用户
