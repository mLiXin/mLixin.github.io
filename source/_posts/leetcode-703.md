---
title: LeetCode.703-Kth Largest Element in a Stream
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories: LeetCode
visible: hide
date: 2019-10-02 19:00:01
---
###### Question
- Source
	- [703. Kth Largest Element in a Stream]() 
- Title
	- 703. Kth Largest Element in a Stream 
- Content
	- Design a class to find the kth largest element in a stream. Note that it is the kth largest element in the sorted order, not the kth distinct element.
Your KthLargest class will have a constructor which accepts an integer k and an integer array nums, which contains initial elements from the stream. For each call to the method KthLargest.add, return the element representing the kth largest element in the stream.
<!--more-->

###### Answer
- 思路
	- 优先级队列实现即可。如果要提交结果好，可以用数组实现一个优先级队列，而不是用Java的api
- 时间复杂度
	- O(logN) 	
- 代码实现

	```Java
	class KthLargest {

    PriorityQueue<Integer> queue;
    int maxK = 0;
    public KthLargest(int k, int[] nums) {
        maxK = k;
        queue = new PriorityQueue<>(k);
        
        for (int i = 0 ; i < nums.length;i++){
            add(nums[i]);
        }
    }

    public int add(int val) {
        if (queue.size() < maxK){
            queue.offer(val);
        }else if (queue.peek() < val){
            queue.poll();
            queue.offer(val);
        }
        
        return  queue.peek();
    }
}
	```
- 提交结果
	- Runtime: 61 ms, faster than 60.57% of Java online submissions for Kth Largest Element in a Stream.
	- Memory Usage: 45.3 MB, less than 96.67% of Java online submissions for Kth Largest Element in a Stream.
