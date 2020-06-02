---
title: LeetCode.232-Implement Queue using Stacks
date: 2019-10-02 16:31:35
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
	- [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) 
- Title
	- 232. Implement Queue using Stacks 
- Content
	- Implement the following operations of a queue using stacks.
		- push(x) -- Push element x to the back of queue.
		- pop() -- Removes the element from in front of queue.
		- peek() -- Get the front element.
		- empty() -- Return whether the queue is empty.
<!--more-->

###### Answer
- 思路
	- 两个栈实现即可
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	class MyQueue {

    Stack<Integer> inStack = new Stack<>();
    Stack<Integer> outStack = new Stack<>();

    /** Initialize your data structure here. */
    public MyQueue() {

    }

    /** Push element x to the back of queue. */
    public void push(int x) {
        inStack.push(x);
    }

    /** Removes the element from in front of queue and returns that element. */
    public int pop() {
        if (outStack.isEmpty()){
            while (!inStack.isEmpty()){
                outStack.push(inStack.pop());
            }
        }

        return outStack.pop();
    }

    /** Get the front element. */
    public int peek() {
        if (outStack.isEmpty()){
            while (!inStack.isEmpty()){
                outStack.push(inStack.pop());
            }
        }
        
        return outStack.peek();
    }

    /** Returns whether the queue is empty. */
    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }
}
	```
- 提交结果
	- Runtime: 42 ms, faster than 81.10% of Java online submissions for Implement Queue using Stacks.
	- Memory Usage: 34.1 MB, less than 20.83% of Java online submissions for Implement Queue using Stacks. 
