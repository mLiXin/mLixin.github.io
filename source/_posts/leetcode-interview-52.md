---
title: LeetCode.面试题52-两个链表的第一个公共节点
date: 2020-04-14 10:30:52
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
	- [面试题52. 两个链表的第一个公共节点]() 
- Title
	- 面试题52. 两个链表的第一个公共节点 
- Content
	- 输入两个链表，找出它们的第一个公共节点。 
<!--more-->

###### Answer
- 思路
	- 两个链表长度不一致，先遍历一遍计算出链表的长度，将长链和短链一致的地方开始遍历即可
- 时间复杂度
	- O(Math.max(n,m)) 	
- 代码实现

	```Java
	public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        int countA = 0;
        int countB = 0;

        ListNode tempA = headA;
        ListNode tempB = headB;

        while(tempA != null){
            countA++;
            tempA = tempA.next;
        }

        while(tempB != null){
            countB ++;
            tempB = tempB.next;
        }

        // A链长
        tempA = headA;
        tempB = headB;
        if(countA > countB){
            int k = countA - countB;
            while(k >0){
                tempA = tempA.next;
                k--;
            }
        }else{
            int k = countB - countA;
            while(k >0){
                tempB = tempB.next;
                k--;
            }
        }

        while(tempA != null && tempA != tempB){
            tempA = tempA.next;
            tempB = tempB.next;
        }

        return tempA;
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :42.7 MB, 在所有 Java 提交中击败了100.00%的用户
