---
title: LeetCode.445-两数相加 II
date: 2020-04-14 10:07:15
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
	- [445. 两数相加 II](https://leetcode-cn.com/problems/add-two-numbers-ii/) 
- Title
	- 445. 两数相加 II 
- Content
	- 给你两个 非空 链表来代表两个非负整数。数字最高位位于链表开始位置。它们的每个节点只存储一位数字。将这两数相加会返回一个新的链表。你可以假设除了数字 0 之外，这两个数字都不会以零开头。
	- 进阶
		- 如果输入链表不能修改该如何处理？换句话说，你不能对列表中的节点进行翻转。

<!--more-->

###### Answer
- 思路
	- 反转两个链表之后再相加，相当于从低位往高位相加，得到结果后再反转结果输出即可。注意进位。 
	- 进阶思路：将两个链表的数字入栈后再出栈计算
- 时间复杂度
	- O(Math.max(n,m)) 	
- 代码实现

	```Java
	public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode reverseL1 = reverse(l1);
        ListNode reverseL2 = reverse(l2);

        int carry = 0;
        ListNode reverseResult = new ListNode(0);
        ListNode headResult = reverseResult;
        while(reverseL1 != null || reverseL2 != null){
            int current = carry;
            if(reverseL1 != null){
                current += reverseL1.val;
                reverseL1 = reverseL1.next;
            }

            if(reverseL2 != null){
                current += reverseL2.val;
                reverseL2 = reverseL2.next;
            }

            if(current > 9){
                carry = 1;
            }else{
                carry = 0;
            }
            reverseResult.next = new ListNode(current % 10);
            reverseResult = reverseResult.next;
        }

        if (carry > 0){
            reverseResult.next = new ListNode(carry);
        }

        return reverse(headResult.next);
    }

    public ListNode reverse(ListNode root){
        ListNode pre = null;
        ListNode current = root;
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
	- 执行用时 :2 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :39.8 MB, 在所有 Java 提交中击败了95.83%的用户
