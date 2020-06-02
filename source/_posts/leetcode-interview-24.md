---
title: LeetCode.面试题24-反转链表
date: 2020-04-09 10:14:56
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
	- [面试题24. 反转链表](https://leetcode-cn.com/problems/fan-zhuan-lian-biao-lcof/) 
- Title
	- 面试题24. 反转链表 
- Content
	- 定义一个函数，输入一个链表的头节点，反转该链表并输出反转后链表的头节点。 
<!--more-->

###### Answer
- 思路
	- pre + current + next，反转的时候，current.next = pre；pre = current；current = next；交换即可。 
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public ListNode reverseList(ListNode head) {
        if(head == null){
            return head;
        }
        ListNode pre = null;
        ListNode current = head;
        ListNode next = current.next;

        while(current != null){
            next = current.next;

            current.next = pre;
            pre = current;
            current = next;
        }
        return pre;
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :39.3 MB, 在所有 Java 提交中击败了100.00%的用户
