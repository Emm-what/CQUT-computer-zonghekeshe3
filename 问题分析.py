#coding:utf-8
import ahocorasick


class questionClassify:
    def __init__(self):
        # 全局变量，用于存储对应的实体
        self.list_disease = []  # 疾病名称
        self.list_department = []  # 科室
        self.list_drug = []  # 药品
        self.list_symptoms = []  # 症状
        self.list_check = []  # 检查
        self.list_food = []  # 食物
        self.list_producer = []  # 药品生产商
        self.list_deny = []  # 否定词
        self.list_all = []  # 存放所有实体的集合
        root = 'D:/PYTHON/医疗问答系统/实体/'
        self.list_disease = [i.strip() for i in open(root + '疾病名称.txt', encoding='utf-8') if i.strip()]
        self.list_check = [i.strip() for i in open(root + '疾病检查.txt', encoding='utf-8') if i.strip()]
        self.list_symptoms = [i.strip() for i in open(root + '疾病症状.txt', encoding='utf-8') if i.strip()]
        self.list_department = [i.strip() for i in open(root + '科室.txt', encoding='utf-8') if i.strip()]
        self.list_food = [i.strip() for i in open(root + '食物.txt', encoding='utf-8') if i.strip()]
        self.list_drug = [i.strip() for i in open(root + '药品名称.txt', encoding='utf-8') if i.strip()]
        self.list_producer = [i.strip() for i in open(root + '药品生产商.txt', encoding='utf-8') if i.strip()]
        self.list_deny = [i.strip() for i in open(root + '否定词.txt', encoding='utf-8') if i.strip()]
        self.list_all = set(self.list_drug + self.list_department + self.list_disease + self.list_producer + self.list_symptoms + self.list_check + self.list_food)
        self.actree = self.build_actree(list(self.list_all))
        self.list_symptom_qws = ['症状', '表征', '现象', '症候', '表现']
        self.list_cause_qws = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.list_complications_qws = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.list_food_qws = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品']
        self.list_drug_qws = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.list_prevent_qws = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
                            '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                            '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                            '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                            '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.list_lasttime_qws = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.list_cureway_qws = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.list_cureprob_qws = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医', '治愈率']
        self.list_easyget_qws = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.list_check_qws = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.list_belong_qws = ['属于什么科', '属于', '什么科', '科室', '挂什么科']
        self.list_depart_dis_qws = ['能治什么病', '能检查什么病']
        self.list_drug_prod_qws = ['生产的', '生产商', '什么生产']
        self.list_prod_drug_qws = ['有什么药', '制造了', '生产了什么药']
        self.list_check_dis_qws = ['能检查什么']
        self.list_dis_drug_qws = ['吃什么能治', '什么能治', '什么药有效']
        self.list_sym_dis_qws = ['是什么病', '为什么会', '什么引起', '什么会引起', '什么病']
        self.list_dis_cost = ['钱', '花费', '花']

    # 构造领域树，用于提速
    def build_actree(self, all_word):
        '''
        ahocosick：自动机的意思
        可实现自动批量匹配字符串的作用，即可一次返回该条字符串中命中的所有关键词
        '''
        actree = ahocorasick.Automaton()
        for index, word in enumerate(all_word):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    # 问句过滤
    def question_filter(self, question):
        region_wds = []
        # i的格式(2, (2067, '肺气肿'))，这一步会取出领域内关键词
        for i in self.actree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        # 判断每对儿词之间的关系，选择更详细的加入词典
        # 去除类似于识别到 鸡蛋，鸡蛋粥 中鸡蛋是无用词，去除更短的一个
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        # print(final_wds)
        final_dict = {}
        for word in final_wds:
            # 经过查阅资料，发现in方法用在set中效率最高
            # dict.setdefault（）若存在则追加，若不存在则新建
            if word in set(self.list_disease):
                final_dict.setdefault('disease', []).append(word)
            if word in set(self.list_drug):
                final_dict.setdefault('drug', []).append(word)
            if word in set(self.list_department):
                final_dict.setdefault('department', []).append(word)
            if word in set(self.list_check):
                final_dict.setdefault('check', []).append(word)
            if word in set(self.list_symptoms):
                final_dict.setdefault('symptoms', []).append(word)
            if word in set(self.list_food):
                final_dict.setdefault('food', []).append(word)
            if word in set(self.list_producer):
                final_dict.setdefault('producer', []).append(word)
        return final_dict

    # 匹配问句类型
    def check_words(self, qws, question):
        for word in qws:
            if word in question:
                return True
        return False

    # 问题分类
    def question_classify(self, question):
        data = {}
        # 先对问句进行过滤提取关键词，匹配用户语言想要表达的意思
        medical_dict = self.question_filter(question)
        if not medical_dict:  # 表明用户提问不含任何关键信息，分类为闲聊
            return {}
        data['argus'] = medical_dict
        types = []
        for type_ in medical_dict:
            types.append(type_)
        question_types = []
        # 已知疾病查症状
        if self.check_words(self.list_symptom_qws, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)
        # 已知疾病查原因
        if self.check_words(self.list_cause_qws, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)
        # 已经疾病查并发症
        if self.check_words(self.list_complications_qws, question) and ('disease' in types):
            question_type = 'disease_complication'
            question_types.append(question_type)
        # 已知疾病查食物
        if self.check_words(self.list_food_qws, question) and ('disease' in types):
            food_flag = self.check_words(self.list_deny, question)
            print(food_flag)
            if food_flag:
                question_type = 'disease_bad_food'
                question_types.append(question_type)
            else:
                question_type = 'disease_good_food'
                question_types.append(question_type)
        # 已知疾病查预防
        if self.check_words(self.list_prevent_qws, question) and ('disease' in types):
            question_type = 'disease_prevent'
            question_types.append(question_type)
        # 已经疾病查周期
        if self.check_words(self.list_lasttime_qws, question) and ('disease' in types):
            question_type = 'disease_lasttime'
            question_types.append(question_type)
        # 已知疾病查治疗
        if self.check_words(self.list_cureway_qws, question) and ('disease' in types):
            question_type = 'disease_cureway'
            question_types.append(question_type)
        # 已经疾病查易感人群
        if self.check_words(self.list_easyget_qws, question) and ('disease' in types):
            question_type = 'disease_easyget'
            question_types.append(question_type)
        # 已知疾病查检查项目
        if self.check_words(self.list_check_qws, question) and ('disease' in types):
            question_type = 'disease_check'
            question_types.append(question_type)
        # 已知疾病查检查药品
        if self.check_words(self.list_drug_qws, question) and ('disease' in types):
            question_type = 'disease_drug'
            question_types.append(question_type)
        # 已知疾病查科室
        if self.check_words(self.list_belong_qws, question) and ('disease' in types):
            question_type = 'disease_department'
            question_types.append(question_type)
        # 已知疾病查治愈率
        if self.check_words(self.list_cureprob_qws, question) and ('disease' in types):
            question_type = 'disease_ratio'
            question_types.append(question_type)
        # 已知疾病查费用
        if self.check_words(self.list_dis_cost, question) and ('disease' in types):
            question_type = 'disease_cost'
            question_types.append(question_type)
        # 已知科室查疾病
        if self.check_words(self.list_depart_dis_qws, question) and ('department' in types):
            question_type = 'department_disease'
            question_types.append(question_type)
        # 已知药品查生产商
        if self.check_words(self.list_drug_prod_qws, question) and ('drug' in types):
            question_type = 'drug_producer'
            question_types.append(question_type)
        # 已知生产商查药品
        if self.check_words(self.list_prod_drug_qws, question) and ('producer' in types):
            question_type = 'producer_drug'
            question_types.append(question_type)
        # 已知检查查疾病
        if self.check_words(self.list_check_dis_qws, question) and ('check' in types):
            question_type = 'check_disease'
            question_types.append(question_type)
        # 已知疾病查应该吃的药
        if self.check_words(self.list_dis_drug_qws, question) and ('disease' in types):
            question_type = 'disease_drug'
            question_types.append(question_type)
        # 已知症状查疾病
        if self.check_words(self.list_sym_dis_qws, question) and ('symptoms' in types):
            question_type = 'symptoms_disease'
            question_types.append(question_type)

        data['question_types'] = question_types
        return data


# 主函数
if __name__ == '__main__':
    # question = '总觉得耳朵痒而且嗡嗡响是为什么'
    while 1:
        question = input()
        q = questionClassify()
        data = q.question_classify(question)
        print(data)
