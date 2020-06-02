---
title: LeetCode.024-Swap Nodes in Pairs
date: 2019-09-30 18:09:12
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
	- [24. Swap Nodes in Pairs]() 
- Title
	- 24. Swap Nodes in Pairs 
- Content
	- Given a linked list, swap every two adjacent nodes and return its head.You may not modify the values in the list's nodes, only nodes itself may be changed.
<!--more-->

###### Answer
- 思路
	- 正常反转即可，注意画图查看过程，链别断掉了。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public ListNode swapPairs(ListNode head) {
        ListNode pre = new ListNode(0);
        pre.next = head;
        ListNode temp = pre;
        while(temp.next != null && temp.next.next != null){
            ListNode cur = temp.next;
            ListNode next = temp.next.next;
            
            temp.next = next;
            cur.next = next.next;
            next.next = cur;
            
            temp = cur;
        }
        return pre.next;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Swap Nodes in Pairs.
	- Memory Usage: 34.5 MB, less than 100.00% of Java online submissions for Swap Nodes in Pairs.
