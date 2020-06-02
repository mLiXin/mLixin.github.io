---
title: LeetCode.面试题25-合并两个排序的链表
date: 2020-04-09 10:28:15
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
	- [面试题25. 合并两个排序的链表](https://leetcode-cn.com/problems/he-bing-liang-ge-pai-xu-de-lian-biao-lcof/) 
- Title
	- 面试题25. 合并两个排序的链表 
- Content
	- 输入两个递增排序的链表，合并这两个链表并使新链表中的节点仍然是递增排序的。
<!--more-->

###### Answer
- 思路
	- 比较两个链表链头值大小决定哪个加入结果链表 
- 时间复杂度
	- O(n+m) 	
- 代码实现

	```Java
	public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode head = new ListNode(0);
        ListNode current = head;
        while(l1 != null && l2 != null){
            if(l1.val <= l2.val){
                current.next = l1;
                l1 = l1.next;
            }else{
                current.next = l2;
                l2 = l2.next;
            }
            current = current.next;
        }

        if (l1 != null) {
            current.next = l1;
        }
        if (l2 != null) {
            current.next = l2;
        }

        return head.next;
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了99.52%的用户
	- 内存消耗 :39.7 MB, 在所有 Java 提交中击败了100.00%的用户
