---
title: LeetCode.面试题40-最小的k个数
date: 2020-04-13 13:31:34
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
	- [面试题40. 最小的k个数](https://leetcode-cn.com/problems/zui-xiao-de-kge-shu-lcof/) 
- Title
	- 面试题40. 最小的k个数 
- Content
	- 输入整数数组 arr ，找出其中最小的 k 个数。例如，输入4、5、1、6、2、7、3、8这8个数字，则最小的4个数字是1、2、3、4。 
<!--more-->

###### Answer
- 思路
	- 排序后取前两位即可
- 时间复杂度
	- O(nLogN) 	
- 代码实现

	```Java
	public int[] getLeastNumbers(int[] arr, int k) {
        quickSort(arr, 0, arr.length - 1, k);
        int[] result = new int[k];
        for (int i = 0; i < k; i++) {
            result[i] = arr[i];
        }
        return result;
    }

    public void quickSort(int[] array, int left, int right, int k) {
        if (left >= right || left > k) {
            return;
        }
        int mid = partition(array, left, right);
        quickSort(array, left, mid - 1, k);
        quickSort(array, mid + 1, right, k);
    }

    public int partition(int[] array, int left, int right) {
        int target = array[right];
        int i = left;
        for (int j = left; j <= right; j++) {
            if (array[j] < target) {
                swap(array, i, j);
                i++;
            }
        }

        swap(array, i, right);
        return i;
    }

    public void swap(int[] array, int left, int right) {
        int temp = array[left];
        array[left] = array[right];
        array[right] = temp;
    }
	```
- 提交结果
	- 执行用时 :6 ms, 在所有 Java 提交中击败了75.59%的用户
	- 内存消耗 :41 MB, 在所有 Java 提交中击败了100.00%的用户
