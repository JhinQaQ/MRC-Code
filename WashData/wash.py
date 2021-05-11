#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 11:20
# @Author  : Yang Jin
# @Site    : 
# @File    : wash.py
# @Software: PyCharm

import json
import re
from random import choice
from os import SEEK_END
from tqdm import tqdm

# 删除连续的空格：
# "真           的"
# "这样吧 你加我QQ 我们聊聊  下面就是我的QQ\n\n\n\n\n\n\n评论区"
# 删除回答为不知道的回答：
# "不知道。"
# 删除回答为找我、加我的：
# "我发行的,找我"
# "找我办网贷+2768180006"
# 删除+后跟10位电话号码的：
# "截图我看一眼就知道了+2768180006"
# 删除怎么联系和怎样联系：
# "我这里可以,您怎么联系"
# "和在抖店买了东西,怎样联系商店。"
# 删除留个联系方式、联系方式给我：
# "我这里可以,把你联系方式给我"

f_1 = open(r'E:\数据清洗\经济_sougou_52880.json', mode='r', encoding='utf-8')
f_2 = open(r'E:\数据清洗\wash\经济_sougou_52880(wash).json', mode='w+', encoding='utf-8')
f_3 = open(r'E:\数据清洗\wash\delate.txt', mode='w+', encoding='utf-8')
load_lst_1 = json.load(f_1)


# json_1 = load_lst_1['answer']
def equal(ans):
    if ans == '不知道':
        return True
    else:
        return False


def write_answer(i):
    for an in i['answer']:
        an.replace(' ', '')
        an_sub = re.sub(sub_pattern, '', an)
        pa = re.search(find_pattern, an_sub)
        if pa or an_sub == '' or equal(an_sub):
            i['answer'].remove(an)

    i['answer_num'] = len(i['answer'])
    json_str = json.dumps(i, indent=4, ensure_ascii=False)
    f_2.write(json_str + ',')


def write_answers(i):
    for an in i['answers']:
        an.replace(' ', '')
        an_sub = re.sub(sub_pattern, '', an)
        pa = re.search(find_pattern, an_sub)
        if pa or an_sub == '' or equal(an_sub):
            i['answers'].remove(an)

    i['answers_count'] = len(i['answers'])
    json_str = json.dumps(i, indent=4, ensure_ascii=False)
    f_2.write(json_str + ',')


sub_pattern = r'( )|(\n)'
find_pattern = r'(看不懂|找我|加我|怎么联系|怎样联系|留个联系方式|联系方式给我|跪求|精辟)|(\+|加)[\d]{9,11}'
f_2.write('[')
for i in tqdm(load_lst_1):
    if 'answer' in i:
        write_answer(i)
    if 'answers' in i:
        write_answers(i)

f_2.write(']')
