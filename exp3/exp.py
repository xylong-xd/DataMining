# coding:gbk
def loadData(path=''):
    '''
    ����ԭʼ����
    '''
    f = open(path + 'house-votes-84.data')
    txt = f.read()
    f.close()
    lst_txt = txt.split('\n')

    data = []

    for txt_line in lst_txt:
        tmp = txt_line.split(',')
        data.append(tmp)

    return data


def preProcessing(data, vote_y_n):
    '''
    ����Ԥ����
    �԰� y �� n Ѱ�ҹ�������
    '''
    data_pre = []
    for data_line in data:
        tmp_data = []
        for i in range(1, len(data_line)):
            # �ӵڶ��п�ʼ���������ļ��еļ�¼�뵱ǰ��ѡ��vote_y_n���бȽϣ����ҵ�����ؼ�¼�����±���ȥ
            if (data_line[i] == vote_y_n):
                tmp_data.append(i)

        if (tmp_data == []):
            continue  # �����ǰ��һ����¼��û���κ�һ������vote_y_n��Ӧ��ѡ���ô���洢���б�ֱ�ӽ�����һ����¼�Ĳ���
        data_pre.append(tmp_data)

    return data_pre


def ppreProcessing(data, vote_y_n, party):
    '''
    ����Ԥ����
    �԰� y �� n ����Ա����������Ѱ�ҹ�������
    '''
    data_pre = []
    for data_line in data:
        tmp_data = []
        if data_line[0] == party:
            for i in range(1, len(data_line)):
                # �ӵڶ��п�ʼ���������ļ��еļ�¼�뵱ǰ��ѡ��vote_y_n���бȽϣ����ҵ�����ؼ�¼�����±���ȥ
                if (data_line[i] == vote_y_n):
                    tmp_data.append(i)
        if (tmp_data == []):
            continue  # �����ǰ��һ����¼��û���κ�һ������vote_y_n����������¼���Ƕ�Ӧparty����Ա��Ӧ��ѡ���ô���洢���б�ֱ�ӽ�����һ����¼�Ĳ���
        data_pre.append(tmp_data)

    return data_pre


def rule_mining(data, support, confidence):
    '''
    �ھ��������
    '''
    dic_1 = mining_first(data, support, confidence)
    # print(dic_1)
    dic_2 = mining_second(data, dic_1, support, confidence)
    # print(dic_2)
    dic_before = dic_2

    dic_r = []

    # Ƶ�����������ֹ�������ǲ������µ�Ƶ�������Ϊֹ
    while (dic_before != {}):
        # dict_r����洢����Ƶ��2-���֮�������Ƶ���
        dic_r.append(dic_before)
        dic_3 = mining_third(data, dic_before, support, confidence)
        dic_before = dic_3

    return dic_r
    pass


def mining_first(data, support, confidence):
    '''
    ���е�һ���ھ�
    �ھ��ѡ1-�
    '''
    dic = {}
    count = len(data)
    for data_line in data:
        # �������ݼ��е�ÿһ��ͶƱ����
        for data_item in data_line:
            # ����ÿһ�������е��±꣨��Ӧĳ�����⣩
            if (data_item in dic):
                # �Լ�ֵ�Ե���ʽ���д洢�ͼ���
                dic[data_item] += 1
            else:
                dic[data_item] = 1

    assert (support >= 0) and (support <= 1), 'suport must be in 0-1'
    # ����������֧�ֶ���ֵ��ͶƱ���ݵ������ĵõ�������������С֧�ֶ�ֵ
    val_suport = int(count * support)
    assert (confidence >= 0) and (confidence <= 1), 'coincidence must be in 0-1'
    # �����ֵ���е�ֵ���ڻ���ڵ�ǰ֧�ֶ���ֵ������Խ��ü�ֵ����ΪƵ��1-�����
    dic_1 = {}
    for item in dic:  # �����ÿһ���������ѡ���ģ�y|n�����м�������������ֵ������֧�ֶ�����Ҫ�ļ������Ͱ����ŵ���һ���ֵ���
        if (dic[item] >= val_suport):
            dic_1[item] = dic[item]

    return dic_1


def mining_second(data, dic_before, support, confidence):
    '''
    ���й�������Ķ����ھ�
    �ھ����ѡ2-�

    ע�������ھ������Ƶ����������ֵ����ʽ�洢�ģ��ֵ�ļ���Ƶ�����
    1Ƶ�����1-16����������ʾ��Щ������ԭ���ݼ��е��±ꣻ��Ƶ����������Щ�±��һ��Ԫ��
    ���غ�������Щ���⹲ͬ��ͶƱΪvote_y_n���ֵ��ֵ������������ϳ��ֵĴ���
    '''
    # ÿһ����չƵ�����ʱ�����һ����ʱdict���ڱ�����Щͨ��Ƶ��������㷨�������µ��
    # ���ǻ�Ҫ�����еĽ������֧�ֶ��жϣ�����ȷ���������µ��㷨
    dic = {}
    count = len(data)
    count2 = 0
    for data_line in data:
        # ��ȡԪ������
        count_item = len(data_line)
        # ÿ������ϼ���
        for i in range(0, count_item - 1):
            # ���ѭ��������Ƶ��2-��еĵ�һ��Ԫ�ص�ȡֵ
            for j in range(i + 1, count_item):
                # �ڲ�ѭ��������Ƶ��2-��еĵڶ���Ԫ�ص�ȡֵ
                if (data_line[i] in dic_before and data_line[j] in dic_before):

                    count2 += 1
                    tmp = (data_line[i], data_line[j])
                    if (tmp in dic):
                        # ��ͬ��ʹ�ü�ֵ�Լ��ϼ�����ֻ������ʱԪ���Ƕ�Ԫ��Ԫ��
                        dic[tmp] += 1
                    else:
                        dic[tmp] = 1
                else:
                    continue
                    # ������������һ������Ƶ��1-������ݼ�֦���ԣ�������ɵ����Ƶ��2-�
    # print(dic)
    assert (support >= 0) and (support <= 1), 'suport must be in 0-1'
    assert (confidence >= 0) and (confidence <= 1), 'confidence must be in 0-1'

    dic_2 = {}
    for item in dic:
        count_item0 = dic_before[item[0]]
        count_item1 = dic_before[item[1]]
        # �ж� ֧�ֶ� �� ���Ŷ�
        # �ж����Ŷȵ�ʱ�����һ�������Ԫ�飬�κ�һ�ַ���Ĺ����п��ܣ���Ҫ���бȽ�
        if ((dic[item] >= support * count) and (
                (dic[item] >= confidence * count_item0) or (dic[item] >= confidence * count_item1))):
            dic_2[item] = dic[item]

    return dic_2


def mining_third(data, dic_before, support, confidence):
    '''
    ���й�������������ھ�
    �ھ����ѡ3-�����4-�����n-�
    '''
    # Ƶ����Ĳ���ʹ��Fk-1*Fk-1�Ĳ���
    dic_3 = {}
    for item0 in dic_before:
        # ���ѭ������Ƶ��k-1��е�ĳһ��
        for item1 in dic_before:
            # �ڲ�ѭ������Ƶ��k-1��е���һ��
            if (item0 != item1):
                # print(item0,item1)
                item_len = len(item0)
                equal = True
                tmp_item3 = []
                # �ж�ǰn-1���Ƿ�һ��
                for i in range(item_len - 1):
                    tmp_item3.append(item0[i])
                    if (item0[i] != item1[i]):
                        equal = False
                        break
                if (equal == True):
                    # �������Fk-1�����k-2������ǰ׺����ô�Ͱ���˳�򣬽����������
                    minitem = min(item0[-1], item1[-1])
                    maxitem = max(item0[-1], item1[-1])
                    tmp_item3.append(minitem)
                    tmp_item3.append(maxitem)
                    tmp_item3 = tuple(tmp_item3)
                    dic_3[tmp_item3] = 0
                else:
                    continue
    # print('dic_3:',dic_3)
    # ����ͳ��֧�ֶȵķ���������ÿһ���������ÿ�����ҵ���k��Ƿ��������������
    # �Ƚϵķ������Ƕ����ÿһλ�����жϣ�����һλ�Ƿ�����������

    for data_line in data:
        for item in dic_3:
            is_in = True
            for i in range(len(item)):
                if (item[i] not in data_line):
                    is_in = False

            # �ú�ѡk��е���������������У�����Խ������
            if (is_in == True):
                dic_3[item] += 1

    assert (support >= 0) and (support <= 1), 'suport must be in 0-1'
    assert (confidence >= 0) and (confidence <= 1), 'coincidence must be in 0-1'

    count = len(data)
    dic_3n = {}
    for item in dic_3:
        # ǰһ���֧�ֶȼ������������ڵ����ȥĩβ�����֣�ͨ����ֵ����ԭ�����ֵ��в�ѯ��ֵ
        count_item0 = dic_before[item[:-1]]
        # �ж� ֧�ֶ� �� ���Ŷ�
        if ((dic_3[item] >= support * count) and (dic_3[item] >= confidence * count_item0)):
            dic_3n[item] = dic_3[item]

    return dic_3n


def association_rules(freq_sets, min_conf):
    '''
    ���ݲ�����Ƶ��������������Ŷ�Ҫ��Ĺ���

    :param dict: Ƶ������ֵ�
    :param dict: Ƶ����ֵ��е�Ƶ����б�
    :param min_conf: ��С���Ŷ�
    :return: �����б�
    '''

    rules = []
    max_len = len(freq_sets)

    for k in range(max_len - 1):
        for freq_set in freq_sets[k]:
            for sub_set in freq_sets[k + 1]:
                if set(freq_set).issubset(set(sub_set)):
                    conf = freq_sets[k + 1][sub_set] / freq_sets[k][freq_set]
                    rule = (set(freq_set), set(sub_set) - set(freq_set), conf)
                    if conf >= min_conf:
                        rules.append(rule)
    return rules


if (__name__ == '__main__'):
    data_row = loadData()

    data_y = preProcessing(data_row, 'y')
    data_n = preProcessing(data_row, 'n')
    data_y_republican = ppreProcessing(data_row, 'y', 'republican')
    data_y_democrat = ppreProcessing(data_row, 'y', 'democrat')
    data_n_republican = ppreProcessing(data_row, 'n', 'republican')
    data_n_democrat = ppreProcessing(data_row, 'n', 'democrat')

    # ֧�ֶ�
    support = 0.3
    # ���Ŷ�
    confidence = 0.9

    # �ܵ�y�������������ɵ�y����
    r_y = rule_mining(data_y, support, confidence)
    print('vote `y`:\n', r_y)
    rule_y = association_rules(r_y, confidence)
    print('rule `y`:\n', rule_y)

    r_y_republican = rule_mining(data_y_republican, support, confidence)
    print('vote_republican `y`:\n', r_y_republican)
    rule_y_republican = association_rules(r_y_republican, confidence)
    print('rule_republican `y`:\n', rule_y_republican)

    r_y_democrat = rule_mining(data_y_democrat, support, confidence)
    print('vote_democrat `y`:\n', r_y_democrat)
    rule_y_democrat = association_rules(r_y_democrat, confidence)
    print('rule_democrat `y`:\n', rule_y_democrat)

    # �ܵ�n�������������ɵ�n����
    r_n = rule_mining(data_n, support, confidence)
    print('vote `n`:\n', r_n)
    rule_n = association_rules(r_n, confidence)
    print('rule `n`:\n', rule_n)

    r_n_republican = rule_mining(data_n_republican, support, confidence)
    print('vote_republican `n`:\n', r_n_republican)
    rule_n_republican = association_rules(r_n_republican, confidence)
    print('rule `n`:\n', rule_n_republican)

    r_n_democrat = rule_mining(data_n_democrat, support, confidence)
    print('vote_democrat `n`:\n', r_n_democrat)
    rule_n_democrat = association_rules(r_n_democrat, confidence)
    print('rule_democrat `n`:\n', rule_n_democrat)

    f = open('result_mining.txt', 'w')
    f.write('vote `y`:\n')
    f.write(str(r_y))
    f.write('rule `y`:\n')
    f.write(str(rule_y))

    f.write('\n\nvote `n`:\n')
    f.write(str(r_n))
    f.write('rule `n`:\n')
    f.write(str(rule_y))
    f.close()