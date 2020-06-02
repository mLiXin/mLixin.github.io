---
title: LeetCode.011-Container With Most Water
date: 2019-07-24 09:46:43
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
	- [11.Container With Most Water](https://leetcode.com/problems/container-with-most-water/)
- Title
	- Container With Most Water
- Content 
	- Given n non-negative integers a1, a2, ..., an , where each represents a point at coordinate (i, ai). n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, which together with x-axis forms a container, such that the container contains the most water.
<!--more-->

###### Answer
- 思路
    - 矩形面积取决于矩形两边最小的height[x]和长度。举例一个[0-7]的数组
    - 长度为7，面积为[0~7]
    - 长度为6，面积为[0~6][1~7]
    - 长度为5，面积为[0~5][1~6][2~7]
    - 长度为4，面积为[0~4][1~5][2~6][3~7]
    - ...
    - 依次类推，当长度较少1的时候，其实可以放弃矮边的所有case。
- 时间复杂度
    - O(n)
- 空间复杂度
    - O(1)
- 代码实现

	```Java
	    public int maxArea(int[] height) {
        int left = 0;
        int right = height.length - 1;

        int max = 0;
        while (left < right) {
            int current = (right - left) * Math.min(height[left], height[right]);
            if (max < current) {
                max = current;
            }
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }

        return max;
    }
	```
- 提交结果
   -  Runtime: 2 ms, faster than 94.41% of Java online submissions for Container With Most Water.
	- Memory Usage: 40.4 MB, less than 83.69% of Java online submissions for Container With Most Water.