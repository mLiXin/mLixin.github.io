---
title: LeetCode.1024-Video Stitching
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories: LeetCode
visible: hide
date: 2019-10-12 09:32:58
---
###### Question
- Source
	- [1024. Video Stitching](https://leetcode.com/problems/video-stitching/) 
- Title
	- 1024. Video Stitching 
- Content
	- You are given a series of video clips from a sporting event that lasted T seconds.  These video clips can be overlapping with each other and have varied lengths.
Each video clip clips[i] is an interval: it starts at time clips[i][0] and ends at time clips[i][1].  We can cut these clips into segments freely: for example, a clip [0, 7] can be cut into segments [0, 1] + [1, 3] + [3, 7].
Return the minimum number of clips needed so that we can cut the clips into segments that cover the entire sporting event ([0, T]).  If the task is impossible, return -1.
<!--more-->

###### Answer
- 思路
	- 状态转移表来实现，多次遍历数组，每次找到情况允许的最大leftPos，用一个tagArray存放，最后遍历tagArray即可
- 时间复杂度
	- O(n2) 	
- 代码实现

	```Java
	public int videoStitching(int[][] clips, int T) {

        int[] tagArray = new int[clips.length];

        int left = 0;
        int right = 0;
        int prePos;
        int i = 0;
        for (; i < clips.length; i++) {

            prePos = -1;
            for (int j = 0; j < clips.length; j++) {

                if (clips[j][0] <= left && clips[j][1] > right) {
                    right = clips[j][1];
                    tagArray[j]++;
                    if (prePos >= 0) {
                        tagArray[prePos]--;
                    }
                    prePos = j;
                }

            }
            if (right >= T) {
                break;
            }

            left = right;
        }

        if (i >= clips.length || right < T) {
            return -1;
        }

        int count = 0;
        for (int j = 0; j < tagArray.length; j++) {
            if (tagArray[j] == 1) {
                count++;
            }
        }
        return count;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Video Stitching.
	- Memory Usage: 34.2 MB, less than 50.00% of Java online submissions for Video Stitching.
