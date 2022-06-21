# coding = utf-8
"""
    Created on 2022年6月21日           
    @author：wensidan 11903990616
    @description： 本程序用于将提取到得实体信息 以及问句类型转换为查询语句，在数据库中查询结果
"""

from py2neo import Graph, NodeMatcher, RelationshipMatcher
from 问题分析 import questionClassify


def search_res(question, graph):
    q = questionClassify()
    data = q.question_classify(question)
    dict_entity = data['argus']
    list_type = data['question_types']
    print(dict_entity)
    print(list_type)
    node_matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)
    for name1 in dict_entity:
        # 找到对应疾病名字的节点
        try:
            for name in dict_entity[name1]:
                if name1 == 'disease':  # 已知疾病
                    node1 = node_matcher.match(name1).where(name=name).first()
                    if list_type[0] == 'disease_symptom':  # 询问症状
                        relationship = list(relationship_matcher.match([node1], r_type='disease_symptoms'))
                        if len(relationship) != 0:
                            temp = name + "的症状有："
                            for i in range(len(relationship)):
                                temp += str(relationship[i].end_node['symptoms_item']) + ' '
                            return temp
                        else:
                            return str(node1['symptoms'])
                    if list_type[0] == 'disease_cause':
                        return str(node1['cause'])
                    if list_type[0] == 'disease_complication':
                        relationship = list(relationship_matcher.match([node1], r_type='complications'))
                        if relationship is not None:
                            temp = name + "的并发症有："
                            for i in range(len(relationship)):
                                temp += str(relationship[i].end_node['name']) + ' '
                            return temp
                        else:
                            return '暂时没有并发症哦'
                    if list_type[0] == 'disease_good_food':
                        relationship = list(relationship_matcher.match([node1], r_type='disease_good_eat'))
                        if len(relationship) != 0:
                            temp = name + "可以吃："
                            for i in range(len(relationship)):
                                temp += str(relationship[i].end_node['food']) + '    '
                            return temp
                        else:
                            return str(node1['good_eat'])
                    if list_type[0] == 'disease_bad_food':
                        relationship = list(relationship_matcher.match([node1], r_type='disease_bad_eat'))
                        if len(relationship) != 0:
                            temp = name + "不可以吃："
                            for i in range(len(relationship)):
                                temp += str(relationship[i].end_node['food']) + '    '
                            return temp
                        else:
                            return str(node1['bad_eat'])

                    if list_type[0] == 'disease_prevent':
                        return str(node1['prevention'])

                    if list_type[0] == 'disease_lasttime':
                        return str(node1['treatment_cycle'])

                    if list_type[0] == 'disease_cureway':
                        return str(node1['cure'])

                    if list_type[0] == 'disease_ratio':
                        return str(node1['recovery_rate'])
                        # print()

                    if list_type[0] == 'disease_easyget':
                        return str(node1['susceptible'])

                    if list_type[0] == 'disease_check':
                        relationship = list(relationship_matcher.match([node1], r_type='disease_check'))
                        if relationship is not None:
                            temp = name + "要检查："
                            for i in range(len(relationship)):
                                temp += str(relationship[i].end_node['check_item']) + '    '
                            return temp
                        else:
                            return str(node1['check'])

                    if list_type[0] == 'disease_cost':
                        return str(node1['cost_of_treatment'])

                    if list_type[0] == 'disease_drug':
                        relationship = list(relationship_matcher.match([node1], r_type='disease_sale_drug'))
                        if relationship is not None:
                            temp = "治疗" + name + "的药品有："
                            dou = []
                            for i in range(len(relationship)):
                                if str(relationship[i].end_node['drug']) not in dou:
                                    dou.append(str(relationship[i].end_node['drug']))
                                    temp += str(relationship[i].end_node['drug']) + ' '
                            return temp

                    if list_type[0] == 'disease_department':
                        relationship = list(relationship_matcher.match([node1], r_type='department'))
                        temp = name + "需要挂的科室："
                        # print(name + "需要挂的科室：")
                        for i in range(len(relationship)):
                            temp += str(relationship[i].end_node['department']) + '  '
                        return temp

                # 已知科室查疾病
                if name1 == 'department':
                    node1 = node_matcher.match(name1).where(department=name).first()
                    if list_type[0] == 'department_disease':
                        relationship = list(relationship_matcher.match([node1], r_type='department_for'))
                        if relationship is None:
                            return "对不起，没有找到您的信息"
                        else:
                            temp = name + "可以看的疾病名称："
                            dou = []
                            for i in range(len(relationship)):
                                if str(relationship[i].end_node['name']) not in dou:
                                    dou.append(str(relationship[i].end_node['name']))
                                    temp += str(relationship[i].end_node['name']) + '  '
                            return temp

                if name1 == 'drug':
                    # 已知药品查找生产商
                    node1 = node_matcher.match(name1).where(drug=name).first()
                    if list_type[0] == 'drug_producer':
                        relationship = list(relationship_matcher.match([node1], r_type='drug_producer'))
                        if relationship is None:
                            return "对不起，没有找到您的信息"
                        else:
                            temp = name + "的生产商有："
                            dou = []
                            for i in range(len(relationship)):
                                if str(relationship[i].end_node['producer']) not in dou:
                                    dou.append(str(relationship[i].end_node['producer']))
                                    temp += str(relationship[i].end_node['producer']) + '  '
                            return temp

                if name1 == 'producer':
                    # 已知生产商查药品
                    node1 = node_matcher.match(name1).where(producer=name).first()
                    if list_type[0] == 'producer_drug':
                        relationship = list(relationship_matcher.match([node1], r_type='producer_drug'))
                        if relationship is None:
                            return "对不起，没有找到您的信息"
                        else:
                            temp = name + "生产的药品有："
                            dou = []
                            for i in range(len(relationship)):
                                if str(relationship[i].end_node['drug']) not in dou:
                                    dou.append(str(relationship[i].end_node['drug']))
                                    temp += str(relationship[i].end_node['drug']) + '  '
                            return temp

                if name1 == 'check':
                    # 已知检查查疾病
                    node1 = node_matcher.match(name1).where(check_item=name).first()
                    if list_type[0] == 'check_disease':
                        relationship = list(relationship_matcher.match([node1], r_type='check_disease'))
                        if relationship is None:
                            return "对不起，没有找到您的信息"
                        else:
                            temp = name + "可以检查的疾病有："
                            dou = []
                            for i in range(len(relationship)):
                                if str(relationship[i].end_node['name']) not in dou:
                                    dou.append(str(relationship[i].end_node['name']))
                                    temp += str(relationship[i].end_node['name']) + '  '
                            return temp

                if name1 == 'symptoms':
                    # 已知症状查疾病
                    node1 = node_matcher.match('symptom').where(symptoms_item=name).first()
                    if list_type[0] == 'symptoms_disease':
                        relationship = list(relationship_matcher.match([node1], r_type='symptoms_disease'))
                        if relationship is None:
                            return "对不起，没有找到您的信息"
                        else:
                            temp = name + "可能的疾病有："
                            for i in range(len(relationship)):
                                temp += str(relationship[i].end_node['name']) + '  '
                            return temp
        except:
            continue


if __name__ == '__main__':

    # 连接数据库
    graph = Graph("http://localhost:7474", auth=("neo4j", "11903990616"))

    while 1:
        question = input("您想咨询什么呢？")
        res = search_res(question, graph)
        print(res)
