---
title: LeetCode.面试题30-包含min函数的栈
date: 2020-04-13 10:18:16
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
	- [面试题30. 包含min函数的栈](https://leetcode-cn.com/problems/bao-han-minhan-shu-de-zhan-lcof/) 
- Title
	- 面试题30. 包含min函数的栈 
- Content
	- 定义栈的数据结构，请在该类型中实现一个能够得到栈的最小元素的 min 函数在该栈中，调用 min、push 及 pop 的时间复杂度都是 O(1)。 
<!--more-->

###### Answer
- 思路
	- 创建两个栈，一个实际存数据的栈，一个存栈中最小元素，每次进栈时候比较元素和最小栈栈顶元素，并入栈较小的那一个即可。可以用数组模拟栈来优化执行时间。
- 时间复杂度
	- O(1) 	
- 代码实现

	```Java
	class MinStack {

    Stack<Integer> stack = new Stack<>();
    Stack<Integer> minStack = new Stack<>();
    /** initialize your data structure here. */
    public MinStack() {

    }
    
    public void push(int x) {
        stack.push(x);
        if(minStack.isEmpty()){
            minStack.push(x);
        }else{
            int currentMin = minStack.peek();
            if(currentMin < x){
                minStack.push(currentMin);
            }else{
                minStack.push(x);
            }
        }
    }
    
    public void pop() {
        stack.pop();
        minStack.pop();
    }
    
    public int top() {
        if(stack.isEmpty()){
            return -1;
        }
        return stack.peek();
    }
    
    public int min() {
        if(minStack.isEmpty()){
            return -1;
        }
        return minStack.peek();
    }
}
	```
- 提交结果
	- 执行用时 :20 ms, 在所有 Java 提交中击败了63.84%的用户
	- 内存消耗 :42 MB, 在所有 Java 提交中击败了100.00%的用户
