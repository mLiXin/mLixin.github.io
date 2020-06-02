---
title: LeetCode.面试题18-删除链表的节点
date: 2020-04-08 10:19:15
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
	- [面试题18. 删除链表的节点](https://leetcode-cn.com/problems/shan-chu-lian-biao-de-jie-dian-lcof/) 
- Title
	- 面试题18. 删除链表的节点 
- Content
	- 给定单向链表的头指针和一个要删除的节点的值，定义一个函数删除该节点。返回删除后的链表的头节点。
<!--more-->

###### Answer
- 思路
	- 如果头结点的值等于target，直接返回头结点的next节点；否则遍历链表，如果current.next.val = val，说明下一个节点是要删除的节点，直接删除该节点即可。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public ListNode deleteNode(ListNode head, int val) {
        ListNode temp = head;
        if(temp.val == val){
            return head.next;
        }
        while(temp.next != null){
            if(temp.next.val == val){
                break;
            }
            temp = temp.next;
        }
        temp.next = temp.next.next;
        return head;
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :39.4 MB, 在所有 Java 提交中击败了100.00%的用户
