---
title: LeetCode.225-Implement Stack using Queues
date: 2019-10-02 16:39:07
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
	- [225. Implement Stack using Queues]() 
- Title
	- 225. Implement Stack using Queues 
- Content
	- Implement the following operations of a stack using queues.
		- push(x) -- Push element x onto stack.
		- pop() -- Removes the element on top of the stack.
		- top() -- Get the top element.
		- empty() -- Return whether the stack is empty.
<!--more-->

###### Answer
- 思路
	- 入队的时候，将入列前面的元素都出队然后入队到当前元素的后面
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	class MyStack {

    Queue<Integer> queue = new LinkedList<>();
    /** Initialize your data structure here. */
    public MyStack() {

    }

    /** Push element x onto stack. */
    public void push(int x) {
        queue.add(x);
        for (int i =0;i<queue.size()-1;i++){
            queue.add(queue.poll());
        }
    }

    /** Removes the element on top of the stack and returns that element. */
    public int pop() {
        return queue.poll();
    }

    /** Get the top element. */
    public int top() {
        return queue.peek();
    }

    /** Returns whether the stack is empty. */
    public boolean empty() {
        return queue.isEmpty();
    }
}
	```
- 提交结果
	- Runtime: 43 ms, faster than 35.50% of Java online submissions for Implement Stack using Queues.
	- Memory Usage: 33.9 MB, less than 91.67% of Java online submissions for Implement Stack using Queues. 
