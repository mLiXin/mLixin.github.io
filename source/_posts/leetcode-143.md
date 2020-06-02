---
title: LeetCode.143-Reorder List
date: 2019-11-19 09:58:55
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
	- [143. Reorder List]() 
- Title
	- 143. Reorder List 
- Content
	- Given a singly linked list L: L0→L1→…→Ln-1→Ln,
reorder it to: L0→Ln→L1→Ln-1→L2→Ln-2→…
	You may not modify the values in the list's nodes, only nodes itself may be changed.
<!--more-->

###### Answer
- 思路
	- 找到中间结点，将后半段链表reverse，然后拉链式合并两个链表即可
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	public void reorderList(ListNode head) {
        if (head == null || head.next == null) {
            return;
        }

        ListNode slow = head;
        ListNode fast = head.next;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        ListNode waitReverse = slow.next;
        slow.next = null;

        waitReverse = reverseNode(waitReverse);

        ListNode result = head;
        ListNode realResult = result;
        while (waitReverse != null) {
            ListNode next = result.next;
            result.next = waitReverse;
            waitReverse = waitReverse.next;
            result = result.next;
            result.next = next;
            result = result.next;
        }
    }

    public ListNode reverseNode(ListNode node) {

        ListNode prev = null;
        ListNode next;
        while (node != null) {
            next = node.next;
            node.next = prev;
            prev = node;
            node = next;
        }
        return prev;
    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 99.95% of Java online submissions for Reorder List.
	- Memory Usage: 39.5 MB, less than 97.73% of Java online submissions for Reorder List. 
