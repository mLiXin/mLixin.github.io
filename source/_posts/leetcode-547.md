---
title: LeetCode.547-Friend Circles
date: 2019-10-12 17:33:56
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
	- [547. Friend Circles](https://leetcode.com/problems/friend-circles/) 
- Title
	- 547. Friend Circles 
- Content
	- There are N students in a class. Some of them are friends, while some are not. Their friendship is transitive in nature. For example, if A is a direct friend of B, and B is a direct friend of C, then A is an indirect friend of C. And we defined a friend circle is a group of students who are direct or indirect friends.
	- Given a N*N matrix M representing the friend relationship between students in the class. If M[i][j] = 1, then the ith and jth students are direct friends with each other, otherwise not. And you have to output the total number of friend circles among all the students.
<!--more-->

###### Answer
- 思路
	- 注意审题，这里的朋友关系是可以传递的，和有个数小岛的题目意思不一样。
- 时间复杂度
	- O(n2) 	
- 代码实现

	```Java
	public int findCircleNum(int[][] M) {
        if (M == null || M.length == 0){
            return 0;
        }

        boolean[] visited = new boolean[M.length];

        int count = 0;
        for (int i = 0; i < M.length; i++) {
            if (!visited[i]) {
                dfs(M, visited, i);
                count++;
            }
        }

        return count;
    }

    public void dfs(int[][] M, boolean[] visited, int i) {
        for (int j = 0; j < M[i].length; j++) {
            if (M[i][j] == 1 && !visited[j]) {
                visited[j] = true;
                dfs(M, visited, j);
            }
        }
    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 100.00% of Java online submissions for Friend Circles.
	- Memory Usage: 43.6 MB, less than 48.00% of Java online submissions for Friend Circles.
