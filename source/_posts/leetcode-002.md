---
title: LeetCode.002-Add Two Numbers
date: 2019-06-17 16:40:27
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
	- [2.Add Two Numbers](https://leetcode.com/problems/add-two-numbers/submissions/)
- Title	
	- Add Two Numbers
- Content
	- You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.You may assume the two numbers do not contain any leading zero, except the number 0 itself.

<!--more-->
###### Answer
- 思路
	- 逆序存储，则头结点为个位，尾结点为最高位；
	- 两数相加为对应位上的和加上低位的进位，故可以直接遍历链表进行相加，并处理进位即可；
	- 注意两个数可能长度不一致，遍历完后注意可能还有进位要处理。
- 时间复杂度
	- `O(n)`
- 空间复杂度
	- `O(1)` 
- 代码实现

	```
	public ListNode addTwoNumbers(ListNode l1, ListNode l2) {

        ListNode head = new ListNode(0);
        ListNode currentNode = head;

        int carry = 0;

        while (l1 != null || l2 != null) {
            int currentSum = carry;

            if (l1 != null) {
                currentSum += l1.val;
            }

            if (l2 != null) {
                currentSum += l2.val;
            }

            carry = currentSum > 9 ? 1 : 0;
            currentNode.next = new ListNode(currentSum > 9 ? currentSum - 10 : currentSum);
            currentNode = currentNode.next;

            if (l1 != null) {
                l1 = l1.next;
            }

            if (l2 != null) {
                l2 = l2.next;
            }
        }

        if (carry > 0) {
            currentNode.next = new ListNode(carry);
        }
        return head.next;
    }
	```
- 提交结果
	- Runtime: 2 ms, faster than 86.62% of Java online submissions for Add Two Numbers.
	- Memory Usage: 43.6 MB, less than 86.91% of Java online submissions for Add Two Numbers.

###### Best Answer
- 代码

	```
	class Solution {
    	public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        	//ListNode result = new ListNode(0);
        	return addRec(l1,l2,0);
    	}
    
    	public ListNode addRec(ListNode l1, ListNode l2, int carry){
        	if(l1==null &&l2==null && carry==0)return null;
        	int sum = carry;
        	if(l1!=null)sum+=l1.val;
        	if(l2!=null)sum+=l2.val;
        	ListNode result = new ListNode(sum%10);
        
        	result.next = addRec(l1!=null? l1.next:null, l2!=null? l2.next:null, sum/10);

        	return result;
  	  	}
	}
	```
- 提交结果	
	- Runtime: 1 ms, faster than 100.00% of Java online submissions for Add Two Numbers.
	- Memory Usage: 44.5 MB, less than 84.93% of Java online submissions for Add Two Numbers.
- 分析
	- 递归实现，减少了链表指向下一个node的操作(`currentNode = currentNode.next;`)
	
