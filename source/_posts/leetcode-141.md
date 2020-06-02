---
title: LeetCode.141-Linked List Cycle
date: 2019-09-30 18:31:37
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
	- [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) 
- Title
	- 141. Linked List Cycle 
- Content
	- Given a linked list, determine if it has a cycle in it.
	To represent a cycle in the given linked list, we use an integer pos which represents the position (0-indexed) in the linked list where tail connects to. If pos is -1, then there is no cycle in the linked list.
<!--more-->

###### Answer
- 思路
	- 快慢指针
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public boolean hasCycle(ListNode head) {
        ListNode fast = head;
        ListNode slow = fast;
        while(fast != null){
            fast = fast.next;
            slow = slow.next;
            
            if(fast != null){
                fast = fast.next;
                
                if(fast == slow){
                    return true;
                }
            }
        }
        
        return false;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Linked List Cycle.
	- Memory Usage: 37.1 MB, less than 100.00% of Java online submissions for Linked List Cycle.
