---
title: LeetCode.093-Restore IP Addresses
date: 2019-10-14 11:55:28
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
	- [93. Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/) 
- Title
	- 93. Restore IP Addresses 
- Content
	- Given a string containing only digits, restore it by returning all possible valid IP address combinations.
<!--more-->

###### Answer
- 思路
	- 回溯算法，ip是固定的四段，每段开始不为0，且都不大于255。根据这些规律去进行回溯处理。
- 时间复杂度
	- O(n2) 	
- 代码实现

	```Java
	List<String> result = new ArrayList<>();

    public List<String> restoreIpAddresses(String s) {
        int length = s.length();
        backtrack(s, 0, "", 4, length);
        return result;
    }

    private void backtrack(String s, int charPos, String tmp, int leftIpCount, int length) {
        if (charPos == length && leftIpCount == 0) {
            result.add(tmp.substring(0, tmp.length() - 1));
            return;
        }
        if (leftIpCount < 0) {
            return;
        }
        for (int j = charPos; j < charPos + 3; j++) {
            if (j < length) {
                // 如果第一个是0，则必须不是当前ip段
                if (charPos == j && s.charAt(j) == '0') {
                    backtrack(s, j + 1, tmp + s.charAt(j) + ".", leftIpCount - 1, length);
                    break;
                }

                // 从开始到这里数字小于等于255，都可以为当前且可回溯
                if (Integer.parseInt(s.substring(charPos, j + 1)) <= 255) {
                    backtrack(s, j + 1, tmp + s.substring(charPos, j + 1) + ".", leftIpCount - 1, length);
                }

            }
        }
    }
	```
- 提交结果
	- Runtime: 2 ms, faster than 91.46% of Java online submissions for Restore IP Addresses.
	- Memory Usage: 41.8 MB, less than 6.98% of Java online submissions for Restore IP Addresses.
