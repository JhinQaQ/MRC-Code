#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/28 18:05
# @Author  : Yang Jin
# @Site    :
# @File    : cutTrain.py
# @Software: PyCharm

import json
import random
import re
from random import choice

# 源数据
f_1 = open(r'E:\比赛\Data\originData\505concat_transfer-33257.json', mode='r', encoding='utf-8')
f_2 = open(r'E:\比赛\Data\transferData\train.txt', mode='w+', encoding='utf-8')
f_4 = open(r'E:\比赛\Data\transferData\temp.txt', mode='w+', encoding='utf-8')
# 用来构建负例的数据
f_3 = open(r'E:\比赛\0429\车主指南QA-63801条.json', mode='r', encoding='utf-8')
load_lst_1 = json.load(f_1)
load_lst_2 = json.load(f_3)
temp = []
append_list = []
jsn = load_lst_1['data'][0]['paragraphs']
# jsn_2 = load_lst_2['data'][0]['paragraphs']


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
    for a in se_lst:
        a_lst = cut_sentence(ans)
        for a_ in a_lst:
            if a_ in a:
                answer_lst.add(a)
    return answer_lst


def no_answer(se_lst, ans):
    no_ans = []
    for a in se_lst:
        if a not in cut_sentence(ans):
            no_ans.append(a)
    return no_ans


def insert(answer, context):
    se_lst = cut_sentence(context)
    an_lst = cut_sentence(answer)
    ra = random.randint(0, len(se_lst) - 1)
    pre_se_lst = se_lst[:ra]
    next_se_lst = se_lst[ra:]
    pre_se_lst.extend(an_lst)
    pre_se_lst.extend(next_se_lst)
    return pre_se_lst


for i in load_lst_2:
    if i['Answers'] != '':
        temp = cut_sentence(i['Answers'])
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
    if not is_im:
        # if len(cut_sentence(context)) < 3:
        #     text['cls'] = 0
        #     text['context'] = context
        #     text['paragraph'] = context
        #     text['title'] = title
        #     if len(text['context']) < 300:
        #         f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
        # else:
        #     text['cls'] = 0
        #     text['context'] = append_list[count]
        #     text['paragraph'] = cut_3_sentences(cut_sentence(context))
        #     text['title'] = title
        #     count = count + 1
        #     if len(text['context']) < 300:
        #         f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
    # else:
        text['cls'] = 1
        if len(cut_sentence(context)) < 3:
            temp_3 = append_list[count]
            count = count + 1
            if len(context) < 300 and len(temp_3) < 300 and context != temp_3:
                text['context'] = context
                text['paragraph'] = context
                text['title'] = title

                f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                # print(text)
                # 负例
                text['context'] = temp_3
                text['cls'] = 0
                text['title'] = title
                f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                # print(text)
                # print('_______________random__________________________')
                # 随机插入
                flag = False
                an_set = set()

                se_lst = insert(context, temp_3)
                se3_lst = cut_3_sentences(se_lst)
                for se in se3_lst:
                    for an in cut_sentence(answer):
                        if an in se:
                            an_set.add(se)
                if len(an_set) != 0:
                    text['context'] = choice(list(an_set))
                    text['cls'] = 1
                    text['title'] = title
                    # f_4.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                    # 负例
                    for an in cut_sentence(text['context']):
                        if an in se_lst:
                            se_lst.remove(an)
                    se3_lst = cut_3_sentences(se_lst)
                    if len(se3_lst) != 0:
                        f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                        # print(text)
                        text['context'] = choice(se3_lst)
                        text['cls'] = 0
                        f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                        # print(text)
                        # print('context小于3')
        else:
            l = list(answer_lst(cut_3_sentences(cut_sentence(context)), answer))
            if len(l) != 0:
                temp_1 = choice(l)
                if len(cut_sentence(context))-len(cut_sentence(answer)) >= 3:
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
                    # if len(text['context']) < 300:
                    f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                    # print(text)
                    # flag = True
                    # 负例
                    text['context'] = temp_2
                    negative = text['context']
                    text['cls'] = 0
                    text['title'] = title
                    # if len(text['context']) < 300 and flag:
                    f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                    # print(text)
                    # print('____________________random____________________')
                    # 随机插入
                    flag = False
                    an_set = set()

                    se_lst = insert(positive, negative)
                    se3_lst = cut_3_sentences(se_lst)
                    for se in se3_lst:
                        for an in cut_sentence(positive):
                            if an in se:
                                an_set.add(se)
                    T_1 = choice(list(an_set))
                    text['context'] = T_1
                    text['cls'] = 1
                    text['title'] = title
                    # f_4.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                    # 负例
                    for an in cut_sentence(text['context']):
                        if an in se_lst:
                            se_lst.remove(an)
                    se3_lst = cut_3_sentences(se_lst)
                    if len(se3_lst) != 0:
                        T_2 = choice(se3_lst)
                        if len(T_1) != 0 and len(T_2) != 0:
                            f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                            # print(text)
                            text['context'] = T_2
                            text['cls'] = 0
                            f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                            # print(text)
                            # print('context大于3')
                            # print('-----------------------------------------')
    temp_1 = None
    temp_2 = None
    temp_3 = None
    se_lst = None
print(count)
