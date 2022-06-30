#!/usr/bin/env python3
# coding: utf-8
# File: 聊天交互.py
# Date: 2022-6-30

from 获取结果 import *
from 问题分析 import *

'''问答类'''
class chat:
    def __init__(self):
        self.graph = Graph("http://localhost:7474", auth=("neo4j", "11903990616"))
        self.classify = questionClassify()

    def chat_main(self, sent):
        answer = '您好，我是小文医药智能助理，希望可以帮到您！祝您身体棒棒！'
        data =  self.classify.question_classify(sent)
        if len(data) == 0:
            return answer
        res = search_res(data, self.graph)
        if not res:
            return answer
        else:
            return '\n'.join(res)

if __name__ == '__main__':
    handler = chat()
    # while 1:
    question = input('用户:')
    answer = handler.chat_main(question)
    print('小文:', answer)

