#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/6 11:10
# @Author  : Yang Jin
# @Site    : 
# @File    : testData.py
# @Software: PyCharm

import json
import re
import random
import copy
f_1 = open(r'E:\比赛\Data\originData\505concat_transfer-33257.json', mode='r', encoding='utf-8')
f_2 = open(r'E:\比赛\Data\transferData\测试集.txt', mode='w+', encoding='utf-8')
# f_3 = open(r'E:\比赛\0429\concat_temp.json', mode='r', encoding='utf-8')
load_lst_1 = json.load(f_1)
# load_lst_2 = json.load(f_3)
append_list = []
jsn_2 = load_lst_1['data'][0]['paragraphs']


def cut_sentence(se):
    sentence_lst = []
    index = re.finditer(r'[。！!?？]', se)
    temp_index = 0
    for k in index:
        # print('why')
        sentence = se[temp_index:k.span()[1]]
        # print(sentence)
        temp_index = k.span()[1]
        sentence_lst.append(sentence)
    return sentence_lst


def index_sentence(se):
    sentence_lst = []
    index = re.finditer(r'[。！!?？]', se)
    # temp_index = 0
    for k in index:
        # print('why')
        # sentence = se[temp_index:k.span()[1]]
        # print(sentence)
        # temp_index = k.span()[1]
        sentence_lst.append(k.span()[1])
    return index


def cut_3_sentences(se_lst):
    setences_lst = []
    # temp_index = 0
    for a in range(len(se_lst) - 2):
        # if se_lst[a] in cut_sentence(answer):
        setences_lst.append(str(se_lst[a] + se_lst[a + 1] + se_lst[a + 2]))
    return setences_lst


# for i in jsn_2:
#     if i['context'] != '':
#         temp = cut_sentence(i['context'])
#     if len(temp) >= 2:
#         for d in cut_3_sentences(temp):
#             append_list.append(d)

count = 0
for i in jsn_2:
    no_answer = []
    text = {}
    answer_lst = []
    answer = ''
    real_answer = i['qas'][0]['answers'][0]['text']
    context = i['context'].replace(' ', '')
    index = index_sentence(context)
    text['question'] = i['qas'][0]['question']
    se_lst = cut_sentence(context)
    # print(se_lst[0])
    if len(se_lst) != 0:
        answer_se = copy.copy(se_lst[0])
    # print(se_lst)
    if len(se_lst) >= 2:
        se_lst.remove(answer_se)
        # print(len(se_lst))
        if len(se_lst) >= 1:
            no_answer = se_lst
            # print(no_answer)
        ra = random.randint(0, len(se_lst) - 1)
        # print(se_lst)
        # print(ra)
        se_lst.insert(ra, answer_se)
        # print(se_lst)
        if ra == len(se_lst) - 1:
            answer_lst = se_lst[ra - 2:ra + 1]
        elif ra == 0:
            answer_lst = se_lst[ra:ra + 3]
        else:
            answer_lst = se_lst[ra - 1:ra + 2]
            # print(answer_lst)
        # answer = ''
        for a in answer_lst:
            answer = answer + a
        text['context'] = real_answer
        text['cls'] = 1
        text['title'] = i['title']
        text['paragraph'] = i['context'].replace(' ', '')
        if len(text['context']) < 300:
            f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
        # 负例
        count = count + 1
        # print(answer_se)
        # print(no_answer)
        for an in cut_sentence(answer):
            if an in no_answer:
                no_answer.remove(an)
        # if answer_se in no_answer:
        #     no_answer.remove(answer_se)
        # print(no_answer)
        if no_answer is not None and len(no_answer) != 0:
            # print(len(no_answer))
            for no_an in range(int(len(no_answer) / 3)+1):
                if 3 * no_an + 2 <= len(no_answer)-1:
                    text['context'] = no_answer[3 * no_an] + no_answer[3 * no_an + 1] + no_answer[3 * no_an + 2]
                    # print(text['context'])
                    text['cls'] = 0
                    text['title'] = i['title']
                    text['paragraph'] = i['context'].replace(' ', '')
                    # no_an = no_an + 2
                    if len(text['context']) < 300:
                        f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                if 3 * no_an + 1 == len(no_answer)-1:
                    text['context'] = no_answer[3 * no_an] + no_answer[3 * no_an + 1]
                    # print(text['context'])
                    text['cls'] = 0
                    text['title'] = i['title']
                    text['paragraph'] = i['context'].replace(' ', '')
                    # no_an = no_an + 2
                    if len(text['context']) < 300:
                        f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
                if 3 * no_an == len(no_answer)-1:
                    text['context'] = no_answer[3 * no_an]
                    # print(text['context'])
                    text['cls'] = 0
                    text['title'] = i['title']
                    text['paragraph'] = i['context'].replace(' ', '')
                    # no_an = no_an + 2
                    if len(text['context']) < 300:
                        f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))

    else:
        text['context'] = real_answer
        text['cls'] = 1
        text['title'] = i['title']
        text['paragraph'] = i['context'].replace(' ', '')
        if len(text['context']) < 300:
            f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
        # 负例
        # count = count + 1
        # if len(no_answer) == 1:
        #     text['context'] = no_answer[0]
        #     text['cls'] = 1
        #     text['title'] = ''
        #     text['paragraph'] = i['content'].replace(' ', '')
        #     if len(text['context']) < 300:
        #         f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))

        # count = count + 1
        # if len(no_answer) != 0:
        #     for no_an in range(len(no_answer)):
        #         if 3*no_an + 2 <= len(no_answer):
        #             text['answer'] = no_answer[3*no_an]+no_answer[3*no_an+1]+no_answer[3*no_an+2]
        #             text['cls'] = 0
        #             # no_an = no_an + 2
        #             if len(text['answer']) < 300:
        #                 f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
        #         if 3*no_an + 1 == len(no_answer):
        #             text['answer'] = no_answer[3*no_an] + no_answer[3*no_an + 1]
        #             text['cls'] = 0
        #             # no_an = no_an + 2
        #             if len(text['answer']) < 300:
        #                 f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
        #         if 3*no_an == len(no_answer):
        #             text['answer'] = no_answer[3*no_an]
        #             text['cls'] = 0
        #             # no_an = no_an + 2
        #             if len(text['answer']) < 300:
        #                 f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))
        # else:
        #     text['answer'] = random.choice(no_answer)
        # text['cls'] = 0
        # if len(text['answer']) < 300:
        #     f_2.write('{}\n'.format(json.dumps(text, ensure_ascii=False)))

print(count)
