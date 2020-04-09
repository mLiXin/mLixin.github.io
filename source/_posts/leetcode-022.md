---
title: LeetCode.022-括号生成
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories:
  - LeetCode
date: 2020-04-09 10:03:14
---
###### Question
- Source
	- [22. 括号生成](https://leetcode-cn.com/problems/generate-parentheses/) 
- Title
	- 22. 括号生成 
- Content
	- 数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。 
<!--more-->

###### Answer
- 思路
	- 回溯法遍历，筛除不符合要求的结果即可。 
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
    List<String> result = new ArrayList<>();

    public List<String> generateParenthesis(int n) {
        generateParenthesis("", n, n);
        return result;
    }

    public void generateParenthesis(String currentResult, int leftCount, int rightCount) {
        if (leftCount > rightCount) {
            return;
        }

        if (leftCount == 0 && rightCount == 0) {
            result.add(currentResult);
            return;
        }

        // 左括号
        if (leftCount >0){
            generateParenthesis(currentResult + "(", leftCount - 1, rightCount);
        }

        // 右括号
        if (rightCount > 0 && leftCount != rightCount){
            generateParenthesis(currentResult + ")", leftCount, rightCount - 1);
        }

    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了98.38%的用户
	- 内存消耗 :39.1 MB, 在所有 Java 提交中击败了5.01%的用户
