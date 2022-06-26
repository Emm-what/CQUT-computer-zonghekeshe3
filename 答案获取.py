# coding = utf-8
"""
    Created on 2021年12月13日
    @author：lizhuohua 11904030126
    @description： 本程序用于将提取到得实体信息 以及问句类型转换为查询语句，在数据库中查询结果
    @version 2.0
"""

from py2neo import Graph, NodeMatcher, RelationshipMatcher
from 问题分析 import questionClassify


def search_res(data, graph):

    dict_entity = data['argus']
    list_type = data['question_types']
    node_matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)
    anwser = []
    # 已知疾病
    if 'disease' in dict_entity:
        entity = 'Disease'
        for name in dict_entity['disease']:
            node1 = node_matcher.match(entity).where(name=name).first()  # 用first取出符合条件的第一个节点
            # 已知疾病查造成原因
            if 'disease_cause' in list_type:
                temp = name + "的造成原因有："
                anwser.append(temp + '、'.join(node1['cause']))
            if 'disease_prevent' in list_type:
                temp = name + "的预防措施有："
                anwser.append(temp + '、'.join(node1['prevent']))
            if 'disease_lasttime' in list_type:
                temp = name + "的发病周期为："
                anwser.append(temp + '、'.join(node1['cure_lasttime']))
            if 'disease_cureprob' in list_type:
                temp = name + "的治愈率："
                anwser.append(temp + '、'.join(node1['cured_prob']))
            if 'disease_cureway' in list_type:
                temp = name + "的治疗措施："
                anwser.append(temp + '、'.join(node1['cure_way']))
            if 'disease_easyget' in list_type:
                temp = name + "的易感人群："
                anwser.append(temp + '、'.join(node1['easy_get']))
            if 'disease_desc' in list_type:
                temp = name + "："
                anwser.append(temp + '、'.join(node1['desc']))
            if 'disease_department' in list_type:
                temp = name + "可挂科室为："
                anwser.append(temp + '、'.join(node1['cure_department']))

            if 'disease_symptom' in list_type:
                relationship = list(relationship_matcher.match([node1], r_type='has_symptom'))
                # print()
                if len(relationship) != 0:
                    temp = name + "的症状通常有："
                    for i in range(len(relationship)):
                        # print('-----', relationship[i])
                        temp += str(relationship[i].end_node['name']) + '、'
                    anwser.append(temp)
                else:
                    anwser.append(str(node1['Symptom']))
            if 'disease_acompany' in list_type:
                relationship = list(relationship_matcher.match([node1], r_type='acompany_with'))
                # print(relationship)
                if len(relationship) != 0:
                    temp = name + "的并发症有："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].end_node) + '、'
                    anwser.append(temp)
                else:
                    anwser.append('暂时没有并发症哦')
            if 'disease_do_food' in list_type:
                relationship = list(relationship_matcher.match([node1], r_type='do_eat'))
                if len(relationship) != 0:
                    temp = name + "可以吃："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].end_node['name']) + '、'
                    anwser.append(temp)
                else:
                    anwser.append(node1['good_eat'])
                relationship = list(relationship_matcher.match([node1], r_type='recommand_eat'))
                if len(relationship) != 0:
                    temp = name + "推荐食谱："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].end_node['name']) + '、'
                    anwser.append(temp)
            if 'disease_not_food' in list_type:
                relationship = list(relationship_matcher.match([node1], r_type='no_eat'))
                if len(relationship) != 0:
                    temp = name + "不可以吃："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].end_node['name']) + '、'
                    anwser.append(temp)
                else:
                    anwser.append(str(node1['bad_eat']))
            if 'disease_check' in list_type:
                relationship = list(relationship_matcher.match([node1], r_type='need_check'))
                if len(relationship) != 0:
                    temp = name + "要检查的项目有："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].end_node['name']) + '、'
                    anwser.append(temp)
                else:
                    anwser.append(str(node1['check']))
            if 'disease_drug' in list_type:
                # anwser.append(str(node1['Drug']))
                relationship = list(relationship_matcher.match([node1], r_type='common_drug'))
                if len(relationship) != 0:
                    temp = name + "通常使用的药品有："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].end_node['name']) + '、'
                    relationship = list(relationship_matcher.match([node1], r_type='recommand_drug'))
                    if len(relationship) != 0:
                        for i in range(len(relationship)):
                            temp += str(relationship[i].end_node['name']) + '、'
                    anwser.append(temp)
    # 已知生产商查药品
    if 'producer' in dict_entity:
        entity = 'Producer'
        for name in dict_entity['producer']:
            node1 = node_matcher.match(entity).where(name=name).first()
            if 'producer_drug' in list_type:
                relationship = list(relationship_matcher.match([node1], r_type='drugs_of'))
                if relationship is None:
                    anwser.append("对不起，没有找到您的信息")
                else:
                    temp = name + "生产的药品有："
                    dou = []
                    for i in range(len(relationship)):
                        temp += str(relationship[i].end_node['name']) + '、'
                    anwser.append(temp)
    #  已知症状查疾病
    if 'symptom' in dict_entity:
        entity = 'Symptom'
        for name in dict_entity['symptom']:
            node1 = node_matcher.match(entity).where(name=name).first()
            # print(node1)
            if 'symptom_disease' in list_type:
                relationship = list(relationship_matcher.match([None, node1], r_type='has_symptom'))
                # print(relationship)
                if len(relationship) != 0:
                    temp = name + '可能由'
                    for i in range(len(relationship)):
                        if i > 8:
                            break
                        temp += str(relationship[i].start_node['name']) + '、'
                    anwser.append(temp + '、、引起，具体情况还需要去医院做详细检查哦！')
    # 已知药品查找生产商
    if 'drug' in dict_entity:
        entity = 'Drug'
        for name in dict_entity['drug']:
            node1 = node_matcher.match(entity).where(name=name).first()
            if 'drug_producer' in list_type:
                relationship = list(relationship_matcher.match([None, node1], r_type='drugs_of'))
                if relationship is None:
                    temp = "对不起，没有找到您的信息"
                else:
                    temp = name + "的生产商有："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].start_node['name']) + '、'
                anwser.append(temp)
            if 'drug_disease' in list_type:
                relationship = list(relationship_matcher.match([None, node1], r_type='recommand_drug'))
                if relationship is None:
                    temp = "对不起，没有找到您的信息"
                else:
                    temp = name + "能治疗的疾病有："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].start_node['name']) + '、'
                anwser.append(temp)

    # 已知检查查疾病
    if 'check' in dict_entity:
        entity = 'Check'
        for name in dict_entity['check']:
            node1 = node_matcher.match(entity).where(name=name).first()

            if 'check_disease' in list_type:
                relationship = list(relationship_matcher.match([None, node1], r_type='need_check'))
                if relationship is None:
                    temp = "对不起，没有找到您的信息"
                else:
                    temp = name + "检查可以检查的疾病有："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].end_node['name']) + '、'
                anwser.append(temp)
    # 已知科室查疾病
    if 'department' in dict_entity:
        entity = 'Department'
        for name in dict_entity['department']:
            node1 = node_matcher.match(entity).where(name=name).first()

            if 'department_disease' in list_type:
                relationship = list(relationship_matcher.match([None, node1], r_type='belongs_to'))
                if relationship is None:
                    temp = "对不起，没有找到您的信息"
                else:
                    temp = name + "检查可以检查的疾病有："
                    for i in range(len(relationship)):
                        temp += str(relationship[i].start_node['name']) + '、'
                anwser.append(temp)
    return anwser

if __name__ == '__main__':

    # 连接数据库
    graph = Graph("http://localhost:7474", auth=("neo4j", "11903990616"))

    while True:
        question = input("请输入您的问题：")
        q = questionClassify()
        data = q.question_classify(question)
        res = search_res(data, graph)
        print(res)
