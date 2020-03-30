---
title: LeetCode.019-Remove Nth Node From End of List
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories: LeetCode
visible: hide
date: 2019-09-18 11:10:38
---
###### Question
- Source
	- [19. Remove Nth Node From End of List]() 
- Title
	- Remove Nth Node From End of List 
- Content
	- Given a linked list, remove the n-th node from the end of list and return its head.
<!--more-->

###### Answer
- 思路
	- 快慢指针，so easy
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode result = new ListNode(0); // 哨兵，简化
        
        ListNode fast = result;
        ListNode slow = result;
        result.next = head;
        for(int i = 0 ; i < n+1;i++){
            fast = fast.next;
        }
        
        while(fast != null){
            slow = slow.next;
            fast = fast.next;
        }
        
        slow.next = slow.next.next;
        return result.next;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Remove Nth Node From End of List.
	- Memory Usage: 34.7 MB, less than 100.00% of Java online submissions for Remove Nth Node From End of List. 
