#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 10:26
# @Author  : Yang Jin
# @Site    : 
# @File    : buildTraining.py
# @Software: PyCharm


import json
import random
import re
from random import choice
from tqdm import tqdm

# 源数据
f_1 = open(r'E:\比赛\Data\originData\512concat_transfer-72683.json', mode='r', encoding='utf-8')
f_2 = open(r'E:\比赛\Data\transferData\train_512.txt', mode='w+', encoding='utf-8')
# 用来构建负例的数据
f_3 = open(r'E:\比赛\0429\车主指南QA-63801条.json', mode='r', encoding='utf-8')

load_lst_1 = json.load(f_1)
load_lst_2 = json.load(f_3)
temp = []
append_list = []
jsn = load_lst_1['data'][0]['paragraphs']


def cut_sentence(se):
    '''

    :param se:句子
    :return: 每句话的集合
    '''

    sentence_lst = []
    index = re.finditer(r'[。!?！？]', se)
    temp_index = 0
    for k in index:
        sentence = se[temp_index:k.span()[1]]
        temp_index = k.span()[1]
        sentence_lst.append(sentence)
    return sentence_lst


def cut_3_sentences(se_lst):
    '''

    :param se_lst:  句子的list
    :return: 包含所有三句话的LIST
    '''
    setences_lst = []
    for a in range(len(se_lst) - 2):
        setences_lst.append(str(se_lst[a] + se_lst[a + 1] + se_lst[a + 2]))
    return setences_lst


def answer_lst(se_lst, ans):
    '''

    :param se_lst: 句子的list
    :param ans: 答案
    :return: 所有包含答案的list
    '''
    answer_lst = set()
    for a in se_lst:
        a_lst = cut_sentence(ans)
        for a_ in a_lst:
            if a_ in a:
                answer_lst.add(a)
    return answer_lst


def no_answer(se_lst, ans):
    '''

    :param se_lst:
    :param ans:
    :return: 所有不包含答案的list
    '''
    no_ans = []
    for a in se_lst:
        if a not in cut_sentence(ans):
            no_ans.append(a)
    return no_ans


for i in load_lst_2:
    if i['Answers'] != '':
        temp = cut_sentence(i['Answers'])
    if len(temp) >= 2:
        for d in cut_3_sentences(temp):
            append_list.append(d)
count = 0
for i in tqdm(jsn):
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
    if not is_im:
        text['cls'] = 1
        # 句子本身没有三句话
        if len(cut_sentence(context)) < 3:
            temp_3 = append_list[count]
            count = count + 1
            if len(context) < 300 and len(temp_3) < 300 and context != temp_3:
                text['context'] = context
                text['paragraph'] = context
                text['title'] = title

                f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                # 负例
                text['context'] = temp_3
                text['cls'] = 0
                text['title'] = title
                f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
        else:
            l = list(answer_lst(cut_3_sentences(cut_sentence(context)), answer))
            if len(l) != 0:
                temp_1 = choice(l)
                if len(cut_sentence(context)) - len(cut_sentence(answer)) >= 3:
                    temp = no_answer(cut_sentence(context), answer)
                    if len(cut_3_sentences(temp)) >= 1:
                        temp_2 = choice(cut_3_sentences(temp))
                    else:
                        temp_2 = append_list[count]
                        count = count + 1
                else:
                    temp_2 = append_list[count]
                    count = count + 1
                if len(temp_1) < 300 and len(temp_2) < 300 and temp_1 != temp_2:
                    text['context'] = temp_1
                    positive = text['context']
                    text['paragraph'] = context
                    text['title'] = title
                    flag = False
                    f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                    # 负例
                    text['context'] = temp_2
                    negative = text['context']
                    text['cls'] = 0
                    text['title'] = title
                    # if len(text['context']) < 300 and flag:
                    f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))

    # temp_1 = None
    # temp_2 = None
    # temp_3 = None
    # se_lst = None
# print(count)
