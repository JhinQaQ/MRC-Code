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


def no_answer(se_lst, ans):
    no_ans = []
    for a in se_lst:
        if a not in cut_sentence(ans):
            no_ans.append(a)


def cut_sentence(se):
    sentence_lst = []
    index = re.finditer(r'[。！!?？；]', se)
    temp_index = 0
    for k in index:
        # print('why')
        sentence = se[temp_index:k.span()[1]]
        # print(sentence)
        temp_index = k.span()[1]
        sentence_lst.append(sentence)
    return sentence_lst


# s = '2134年12月1日 首先需要说明的一点,无论是Winform,还是Webform,都有很成熟的日历控件,无论从易用性还是可扩展性上看,日期的选择和校验还是用日历控件来实现比较好。 前几天在C...'
#
# a = re.sub(r'(\d{4}年\d{1,2}月\d{1,2}日)|(\d{1,2}天前)', '', s)
# # a = re.sub(r'[\d{1,2}天前]', '', s)
# print(a)
# # print(balancedStringSplit("RLRRLLRLRL"))
# ans = '我。啊。你。'
# context = '我。啊。你。w。a。w。'
# print(no_answer(cut_sentence(context), ans))
# sub_pattern = r'( )|(\n)'
# find_pattern = r'(不知道|找我|加我|怎么联系|怎样联系|留个联系方式|联系方式给我|跪求)|(\+|加)[\d]{9,11}'
# a = '找我办网贷+2768180006'
# pa = re.search(find_pattern, a)
# if pa:
#     print('delate')
# else:
#     print(a)

if False:
    print('yes')