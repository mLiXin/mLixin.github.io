---
title: LeetCode.面试题57-II-和为s的连续正数序列
date: 2020-04-15 13:55:03
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
	- [面试题57 - II. 和为s的连续正数序列](https://leetcode-cn.com/problems/he-wei-sde-lian-xu-zheng-shu-xu-lie-lcof/) 
- Title
	- 面试题57 - II. 和为s的连续正数序列 
- Content
	- 输入一个正整数 target ，输出所有和为 target 的连续正整数序列（至少含有两个数）。序列内的数字由小到大排列，不同序列按照首个数字从小到大排列。
<!--more-->

###### Answer
- 思路
	- 要求是连续的子序列，通过滑动窗口处理 
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	// 滑动窗口
    public int[][] findContinuousSequence(int target) {
        List<int[]> list = new ArrayList<>();

        int left = 1;
        int right = 1;
        int sum = 0;

        while(left <= target / 2){
            if( sum < target){
                sum += right;
                right ++;
            }else if(sum > target){
                sum -= left;
                left ++;
            }else {
                int[] current = new int[right - left];
                for(int i = left;i<right;i++){
                    current[i-left] = i;
                }

                list.add(current);
                sum -= left;
                left++;
            }
        }

        return list.toArray(new int[list.size()][]);
    }
	```
- 提交结果
	- 执行用时 :4 ms, 在所有 Java 提交中击败了73.94%的用户
	- 内存消耗 :37.6 MB, 在所有 Java 提交中击败了100.00%的用户
