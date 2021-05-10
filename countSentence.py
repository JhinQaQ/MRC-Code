#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/10 11:02
# @Author  : Yang Jin
# @Site    : 
# @File    : countSentence.py
# @Software: PyCharm

import json
import re
from random import choice

f_1 = open(r'E:\比赛\Data\originData\505concat_transfer-33257.json', mode='r', encoding='utf-8')
f_2 = open(r'E:\比赛\Data\transferData\train_0510.txt', mode='w+', encoding='utf-8')
f_3 = open(r'E:\比赛\Data\transferData\train_0506.txt', mode='r', encoding='utf-8')
load_lst_1 = json.load(f_1)
load_lst_2 = json.load(f_3)
temp = []
append_list = []
jsn = load_lst_1['data'][0]['paragraphs']

answer_1_lst = []
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


count = 0
for i in jsn:
    answer = i['qas'][0]['answers'][0]['text']
    a = len(cut_sentence(answer))
    for a_se in a:
        answer_1_lst.append(a_se)

for i in load_lst_2[:10]:
    print(i['question'])