---
title: LeetCode.004-Median of Two Sorted Arrays
date: 2019-06-18 16:34:48
tags:
- LeetCode
- Algorithm
- Java
- NEED_MORE_ATTENTION
- LeetCode-Hard
categories: LeetCode
visible: hide 
---
###### Question
- Source
	- [4.Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/submissions/) 
- Title
	- Median of Two Sorted Arrays
- Content
	- There are two sorted arrays nums1 and nums2 of size m and n respectively.Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).You may assume nums1 and nums2 cannot be both empty.

<!--more-->
###### Answer
- 思路
	- 中位数是中间的数字或者中间两个数字的平均数
	- 两个数组都已经是有序的，从小到大遍历，比较两个数组当前数字的大小，只需要遍历到中间位置的数即可了。
- 时间复杂度
	- O(m+n)
- 空间复杂度
	- O(1) 
- 代码实现

	```
	// Sorted Arrays
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {

        int nums1Pos = 0;
        int nums2Pos = 0;

        int midPre = 0;
        int midCurrent = 0;

        // 4/2 = 2   1/2
        // 5/2 = 2   2
        for (int i = 0; i <= (nums1.length + nums2.length) / 2; i++) {

            midPre = midCurrent;

            if (nums1Pos == nums1.length) {
                // num1 has traversed
                midCurrent = nums2[nums2Pos];
                nums2Pos++;
            } else if (nums2Pos == nums2.length) {
                // num1 has traversed
                midCurrent = nums1[nums1Pos];
                nums1Pos++;
            } else if (nums1[nums1Pos] <= nums2[nums2Pos]) {
                midCurrent = nums1[nums1Pos];
                nums1Pos++;
            } else {
                midCurrent = nums2[nums2Pos];
                nums2Pos++;
            }
        }

        if ((nums1.length + nums2.length) % 2 == 0) {
            return (midPre + midCurrent) / 2.0;
        }

        return midCurrent;
    }
	```
- 提交结果
	- Runtime: 2 ms, faster than 100.00% of Java online submissions for Median of Two Sorted Arrays.
	- Memory Usage: 47.2 MB, less than 85.12% of Java online submissions for Median of Two Sorted Arrays.

###### Best Answer
- 思路
	- 中位数实际就是从小到大第k大的数字,可以分别对两个数组进行二分查找，比较结果，然后剔除多余的数字。 
	- 中间位置为mid，题目即为求解两个数组中第mid大的数字；若A数组中位置为i的数字比数组B位置为mid-i的数字小，则可以剔除A前i个数字，mid = mid - i; 
- 时间复杂度
	- O(log(m+n)) 
- 代码
	
	```
	// Sorted Arrays
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {

        int length1 = nums1.length;
        int length2 = nums2.length;

        int minK = (nums1.length + nums2.length + 1) / 2;

        if ((length1 + length2) % 2 != 0) {
            return findMedianSortedArrays(nums1, nums2, minK);
        } else {
            return (findMedianSortedArrays(nums1, nums2, minK) + findMedianSortedArrays(nums1, nums2,
                    minK + 1)) / 2.0;
        }
    }

    public double findMedianSortedArrays(int[] nums1, int[] nums2, int minK) {
        // make sure num1's length is smaller than nums2
        if (nums1.length > nums2.length) {
            return findMedianSortedArrays(nums2, nums1, minK);
        }

        
        if (nums1.length == 0) {
            return nums2[minK - 1];
        }
        
        if (minK == 1) {
            return Math.min(nums1[0], nums2[0]);
        }

        int mid1 = Math.min(nums1.length, minK / 2);
        int mid2 = minK - mid1;

        if (nums1[mid1 - 1] < nums2[mid2 - 1]) {
            int[] new1 = new int[nums1.length - mid1];
            System.arraycopy(nums1, mid1, new1, 0, new1.length);
            return findMedianSortedArrays(new1, nums2, minK - mid1);
        } else {
            int[] new2 = new int[nums2.length - mid2];
            System.arraycopy(nums2, mid2, new2, 0, new2.length);
            return findMedianSortedArrays(new2, nums1, minK - mid2);
        }
    }
	```
- 提交结果
	- Runtime: 2 ms, faster than 100.00% of Java online submissions for Median of Two Sorted Arrays.
	- Memory Usage: 48.1 MB, less than 44.07% of Java online submissions for Median of Two Sorted Arrays.