#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/28 18:05
# @Author  : Yang Jin
# @Site    :
# @File    : cutTrain.py
# @Software: PyCharm

import json
import re
from random import choice

# 源数据
f_1 = open(r'E:\比赛\Data\originData\505concat_transfer-33257.json', mode='r', encoding='utf-8')
f_2 = open(r'E:\比赛\Data\transferData\train.txt', mode='w+', encoding='utf-8')
# 用来构建负例的数据
f_3 = open(r'E:\比赛\0429\concat_temp.json', mode='r', encoding='utf-8')
load_lst_1 = json.load(f_1)
load_lst_2 = json.load(f_3)
temp = []
append_list = []
jsn = load_lst_1['data'][0]['paragraphs']
jsn_2 = load_lst_2['data'][0]['paragraphs']


def cut_sentence(se):
    sentence_lst = []
    index = re.finditer(r'[。!?！？]', se)
    temp_index = 0
    for k in index:
        sentence = se[temp_index:k.span()[1]]
        temp_index = k.span()[1]
        sentence_lst.append(sentence)
    return sentence_lst


def cut_3_sentences(se_lst):
    setences_lst = []
    for a in range(len(se_lst) - 2):
        setences_lst.append(str(se_lst[a] + se_lst[a + 1] + se_lst[a + 2]))
    return setences_lst


def answer_lst(se_lst, ans):
    answer_lst = set()
    a_lst = []
    for an in se_lst:
        a_lst = cut_sentence(an)
        for i in a_lst:
            flag = False
            if len(i) <= len(ans):
                if i in ans:
                    flag = True
            else:
                if ans in i:
                    flag = True
            if flag:
                answer_lst.add(an)
    return answer_lst


for i in jsn_2:
    if i['context'] != '':
        temp = cut_sentence(i['context'])
    if len(temp) >= 2:
        for d in cut_3_sentences(temp):
            append_list.append(d)
count = 0
for i in jsn:
    text = {}
    context = i['context']
    context.replace('[', '')
    context.replace(']', '')
    if i.get('title') is not None:
        title = i['title']
    else:
        title = ''
    answer = i['qas'][0]['answers'][0]['text']
    text['question'] = i['qas'][0]['question']
    text['context'] = ""
    is_im = i['qas'][0]['is_impossible']
    flag = False
    if is_im:
        if len(cut_sentence(context)) < 3:
            text['cls'] = 0
            text['context'] = context
            text['paragraph'] = context
            text['title'] = title
            if len(text['context']) < 300:
                f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
        else:
            text['cls'] = 0
            text['context'] = append_list[count]
            text['paragraph'] = cut_3_sentences(cut_sentence(context))
            text['title'] = title
            count = count + 1
            if len(text['context']) < 300:
                f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
    else:
        text['cls'] = 1
        if len(cut_sentence(context)) < 3:
            temp_1 = choice(append_list)
            if len(context)<300 and len(temp_1) < 300:
                text['context'] = context
                text['paragraph'] = context
                text['title'] = title
                # flag = False
                # if len(text['context']) < 300:
                f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                    # flag = True
                # 负例
                text['context'] = temp_1
                text['cls'] = 0
                text['title'] = title
                # if len(text['context']) < 300 and flag:
                f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
        else:
            l = list(answer_lst(cut_3_sentences(cut_sentence(context)), answer))
            if len(l) != 0:
                temp_1 = choice(l)
                temp_2 = append_list[count]
                count = count + 1
                if len(temp_1) < 300 and len(temp_2) < 300:
                    text['context'] = temp_1
                    text['paragraph'] = context
                    text['title'] = title
                    flag = False
                    # if len(text['context']) < 300:
                    f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                        # flag = True
                    # 负例
                    text['context'] = temp_2
                    text['cls'] = 0
                    text['title'] = title
                    # if len(text['context']) < 300 and flag:
                    f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))


print(count)
