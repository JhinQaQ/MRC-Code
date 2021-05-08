#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/7 16:48
# @Author  : Yang Jin
# @Site    : 
# @File    : test.py
# @Software: PyCharm
import re


def balancedStringSplit(s):
    """
    :type s: str
    :rtype: int
    """
    temp_L = "L"
    temp_R = "R"
    count = 0
    for i in range(500):

        if s.find(temp_R) != -1:
            temp = temp_R + temp_L
            count = count + s.count(temp)
            print(s.count(temp_R + temp_L))
        temp_L = temp_L + "L"
        temp_R = temp_R + "R"

    return count


s = '2134年12月1日 首先需要说明的一点,无论是Winform,还是Webform,都有很成熟的日历控件,无论从易用性还是可扩展性上看,日期的选择和校验还是用日历控件来实现比较好。 前几天在C...'

a = re.sub(r'(\d{4}年\d{1,2}月\d{1,2}日)|(\d{1,2}天前)', '', s)
# a = re.sub(r'[\d{1,2}天前]', '', s)
print(a)
# print(balancedStringSplit("RLRRLLRLRL"))
