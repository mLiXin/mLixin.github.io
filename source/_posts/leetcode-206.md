---
title: LeetCode.206-Reverse Linked List
date: 2019-09-30 17:26:44
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
	- [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list) 
- Title
	- 206. Reverse Linked List 
- Content
	- Reverse a singly linked list. 
<!--more-->

###### Answer
- 思路
	- 反转即可，用一个pre指针，一个next指针，一个cur指针，每次将cur的next指向pre，然后cur指向next即可。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public ListNode reverseList(ListNode head) {
        ListNode pre = null;
        ListNode cur = head;
        ListNode next = null;
        
        while(cur != null){
            next = cur.next;
            cur.next = pre;
            pre = cur;
            
            cur = next;
        }
        return pre;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Reverse Linked List.
	- Memory Usage: 36.9 MB, less than 99.28% of Java online submissions for Reverse Linked List. 
