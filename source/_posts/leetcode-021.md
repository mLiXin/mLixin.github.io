---
title: LeetCode.021-Merge Two Sorted Lists 
date: 2019-09-11 11:10:27
tags:
- LeetCode
- Algorithm
- Java
- LeetCode-Easy
categories: LeetCode
visible: hide
---
###### Question
- Source
	- [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) 
- Title
	- Merge Two Sorted Lists 
- Content 
	- Merge two sorted linked lists and return it as a new list. The new list should be made by splicing together the nodes of the first two lists. 
<!--more-->

###### Answer
- 思路
	- 直接对比merge即可 
- 时间复杂度
	- O(n) 
- 代码实现

	```Java
	// 也可以递归实现
	public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode result = new ListNode(0);
        ListNode head = result;
        while(l1 != null && l2 != null){
            if(l1.val < l2.val){
                head.next = l1;
                l1 = l1.next;
            }else{
                head.next = l2;
                l2 = l2.next;
            }
            head = head.next;
        }
        if(l1 != null){
            head.next = l1;
        }
        
        if(l2 != null){
            head.next = l2;
        }
        return result.next;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Merge Two Sorted Lists.
	- Memory Usage: 39.6 MB, less than 16.16% of Java online submissions for Merge Two Sorted Lists.

