#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/10 11:01
# @Author  : Yang Jin
# @Site    : 
# @File    : randomITrain.py
# @Software: PyCharm
import json
import re
from random import choice

f_1 = open(r'E:\比赛\Data\originData\505concat_transfer-33257.json', mode='r', encoding='utf-8')
f_2 = open(r'E:\比赛\Data\transferData\train_0510.txt', mode='w+', encoding='utf-8')
load_lst_1 = json.load(f_1)
temp = []
append_list = []
jsn = load_lst_1['data'][0]['paragraphs']



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

for i in jsn:
    text = {}
    context = i['context']
    title = i['title']
    answer = i['qas'][0]['answers'][0]['text']
    text['question'] = i['qas'][0]['question']
    text['context'] = ""
    is_im = i['qas'][0]['is_impossible']
    # flag = False
    if not is_im:
        text['cls'] = 1
        # for m in cut_3_sentences(cut_sentence(context)):
        m = answer_lst(cut_3_sentences(cut_sentence(context)), answer)
        # print('___________________________________________')
        # print(context)
        if len(m) != 0:
            text['context'] = choice(list(m))
            text['paragraph'] = context
            text['title'] = title
            # flag = False
            if len(text['context']) < 300:
                f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
            # print(m)
            # print(context)
            # 负例
            noAnswer_lst = []
            for a in cut_3_sentences(cut_sentence(context)):
                if a not in m:
                    noAnswer_lst.append(a)
            if len(noAnswer_lst) != 0:
                text['context'] = choice(noAnswer_lst)
                text['cls'] = 0
                text['title'] = title
                # print(noAnswer_lst)

                if len(text['context']) < 300:
                    f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))