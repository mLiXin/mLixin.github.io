---
title: LeetCode.面试题09-用两个栈实现队列
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-03-31 10:23:59
---
###### Question
- Source
	- [面试题09. 用两个栈实现队列]() 
- Title
	- 面试题09. 用两个栈实现队列 
- Content
	- 用两个栈实现一个队列。队列的声明如下，请实现它的两个函数 appendTail 和 deleteHead ，分别完成在队列尾部插入整数和在队列头部删除整数的功能。(若队列中没有元素，deleteHead 操作返回 -1 )
	- 提示：
		- 1 <= values <= 10000
		- 最多会对 appendTail、deleteHead 进行 10000 次调用
<!--more-->

###### Answer
- 思路
	- 创建两个栈，一个入队栈，一个出队栈。appendTail的时候，将元素push到入队栈中；deleteHead的时候，先看出队栈中是否有值，有的话直接pop栈顶，没有的话将入队栈中的元素都pop并push到出队栈中，在从出队栈中pop。
	- 这里的两个栈也可以自己通过数组实现，因为values是有范围的，自定义两个数组来模拟出队、入队栈就好了。
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	class CQueue {

    Stack<Integer> inQueueStack = new Stack<>();
    Stack<Integer> outQueueStack = new Stack<>();
    public CQueue() {

    }

    public void appendTail(int value) {
        inQueueStack.push(value);
    }

    public int deleteHead() {
        if (!outQueueStack.isEmpty()){
            return outQueueStack.pop();
        }else {

            if (inQueueStack.isEmpty()){
                return -1;
            }

            while (!inQueueStack.isEmpty()){
                outQueueStack.push(inQueueStack.pop());
            }

            return outQueueStack.pop();
        }
    }
}
	```
- 提交结果
	- 执行用时 :56 ms, 在所有 Java 提交中击败了86.67%的用户
	- 内存消耗 :46.7 MB, 在所有 Java 提交中击败了100.00%的用户
