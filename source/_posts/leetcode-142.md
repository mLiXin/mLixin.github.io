---
title: LeetCode.142-Linked List Cycle II
date: 2019-10-02 15:17:59
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
	- [142. Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) 
- Title
	- 142. Linked List Cycle II
- Content
	- Given a linked list, return the node where the cycle begins. If there is no cycle, return null.
To represent a cycle in the given linked list, we use an integer pos which represents the position (0-indexed) in the linked list where tail connects to. If pos is -1, then there is no cycle in the linked list.
Note: Do not modify the linked list.
<!--more-->

###### Answer
- 思路
	- 快慢指针法，注意它们重逢的时候，慢指针走过的路程一定小于或等于环的路程，因为快指针是慢指针的两倍，这样去分析。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public ListNode detectCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        
        while(fast != null && fast.next != null){
            slow = slow.next;
            fast = fast.next.next;
            
            if(slow == fast){
                break;
            }
        }
        
        if(fast == null || fast.next == null){
            return null;
        }
        ListNode node1 = head;
        ListNode node2 = fast;
        
        while(node1 != node2){
            node1 = node1.next;
            node2 = node2.next;
        }
        
        return node1;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Linked List Cycle II.
	- Memory Usage: 34.5 MB, less than 92.63% of Java online submissions for Linked List Cycle II. 
