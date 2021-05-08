import re
import os
import csv
import json
import time
import tqdm
import random
from pprint import pprint


def gen_test():
    """
    生成测试集，同时具备正例和反例
    :return:
    """
    # \505concat_transfer-33257.json
    base_dir = r'E:\比赛\Data\originData'
    random.seed(0)
    lst_result = []
    set_question = set()
    for file in os.listdir(base_dir):
        with open(os.path.join(base_dir, file), encoding='utf8') as fr:

            lst_qa = json.load(fr)
            # print(lst_qa)
        for dic in tqdm.tqdm(lst_qa):
            question = dic['Question']
            context = dic['Answers'].replace(' ', '')
            # 过滤太长的context
            if len(context) > 300:
                continue
            # 对问题去重，只留下最佳答案
            if question in set_question:
                continue
            set_question.add(dic['Question'])
            dic_res = {'Question': dic['Question'], 'context': context}
            # 计算context的句数
            lst = []
            string = ''
            for char in context:
                string += char
                if re.match('[。！？]', char):
                    if len(string) > 1 and not re.match('^[。！？]+$', string):
                        lst.append(string)
                        string = ''
            if string:
                lst.append(string)
            # 多于三句，则在自己的context中抽取前三句作为正例，往后滑动抽取三句作为反例
            if len(lst) > 3:
                dic_res['positive_answer'] = ''.join(lst[:3])
                dic_res['negative_answer'] = ''.join(lst[1:])
                dic_res['negative_answer'] = []
                i = 3
                while i + 3 <= len(lst):
                    dic_res['negative_answer'].append(''.join(lst[i:i+3]))
                    i += 3
                if i != len(lst):
                    dic_res['negative_answer'].append(''.join(lst[i:len(lst)]))
            # 不多于三句，则不抽取负例
            else:
                dic_res['positive_answer'] = ''.join(lst[:])
                dic_res['negative_answer'] = ''
            # # 不多于三句，则将自己的context作为正例，随机抽取其它多于三句的context的后三句作为反例
            # else:
            #     dic_res['positive_answer'] = ''.join(lst[:])
            #     index = random.randint(0, len(lst_qa) - 1)
            #     context = lst_qa[index]['Answers'].replace(' ', '')
            #     while lst_qa[index]['Question'] == dic_res['Question'] or not re.match('^.+[。！？].+[。！？].+[。！？].+$', context) or len(context) > 300:
            #         index = random.randint(0, len(lst_qa) - 1)
            #         context = lst_qa[index]['Answers'].replace(' ', '')
            #     lst = []
            #     string = ''
            #     for char in context:
            #         string += char
            #         if re.match('[。！？]', char):
            #             lst.append(string)
            #             string = ''
            #     if string:
            #         lst.append(string)
            #     dic_res['negative_answer'] = ''.join(lst[-3:])
            lst_result.append(dic_res)

    with open(r'E:\比赛\Data\transferData\测试集.txt', 'w', encoding='utf8') as fw:
        for dic in lst_result:
            dic_p = {'question': dic['Question'], 'context': dic['positive_answer'], 'cls': 1, 'paragraph': dic['context'], 'title': ''}
            fw.write(json.dumps(dic_p, ensure_ascii=False) + '\n')
            for n in dic['negative_answer']:
                dic_n = {'question': dic['Question'], 'context': n, 'cls': 0, 'paragraph': dic['context'], 'title': ''}
            # if dic['negative_answer']:
            #     dic_n = {'question': dic['Question'], 'answer': dic['negative_answer'], 'cls': 0, 'paragraph': dic['context'], 'title': ''}
                fw.write(json.dumps(dic_n, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    # gen_test()
    pass
