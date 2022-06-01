# coding:gbk
def loadData(path=''):
    '''
    加载原始数据
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
    数据预处理
    以按 y 或 n 寻找关联规则
    '''
    data_pre = []
    for data_line in data:
        tmp_data = []
        for i in range(1, len(data_line)):
            # 从第二列开始，将数据文件中的记录与当前的选择vote_y_n进行比较，若找到了相关记录，把下标存进去
            if (data_line[i] == vote_y_n):
                tmp_data.append(i)

        if (tmp_data == []):
            continue  # 如果当前这一条记录中没有任何一个项是vote_y_n对应的选项，那么不存储空列表，直接进行下一个记录的查找
        data_pre.append(tmp_data)

    return data_pre


def ppreProcessing(data, vote_y_n, party):
    '''
    数据预处理
    以按 y 或 n 和议员所属党派来寻找关联规则
    '''
    data_pre = []
    for data_line in data:
        tmp_data = []
        if data_line[0] == party:
            for i in range(1, len(data_line)):
                # 从第二列开始，将数据文件中的记录与当前的选择vote_y_n进行比较，若找到了相关记录，把下标存进去
                if (data_line[i] == vote_y_n):
                    tmp_data.append(i)
        if (tmp_data == []):
            continue  # 如果当前这一条记录中没有任何一个项是vote_y_n或者这条记录不是对应party的议员对应的选项，那么不存储空列表，直接进行下一个记录的查找
        data_pre.append(tmp_data)

    return data_pre


def rule_mining(data, support, confidence):
    '''
    挖掘关联规则
    '''
    dic_1 = mining_first(data, support, confidence)
    # print(dic_1)
    dic_2 = mining_second(data, dic_1, support, confidence)
    # print(dic_2)
    dic_before = dic_2

    dic_r = []

    # 频繁项集产生的终止条件就是不再有新的频繁项集产生为止
    while (dic_before != {}):
        # dict_r里面存储的是频繁2-项集及之后的所有频繁项集
        dic_r.append(dic_before)
        dic_3 = mining_third(data, dic_before, support, confidence)
        dic_before = dic_3

    return dic_r
    pass


def mining_first(data, support, confidence):
    '''
    进行第一次挖掘
    挖掘候选1-项集
    '''
    dic = {}
    count = len(data)
    for data_line in data:
        # 对于数据集中的每一行投票数据
        for data_item in data_line:
            # 对于每一行数据中的下标（对应某个议题）
            if (data_item in dic):
                # 以键值对的形式进行存储和计数
                dic[data_item] += 1
            else:
                dic[data_item] = 1

    assert (support >= 0) and (support <= 1), 'suport must be in 0-1'
    # 依靠给定的支持度阈值和投票数据的总数的得到满足条件的最小支持度值
    val_suport = int(count * support)
    assert (confidence >= 0) and (confidence <= 1), 'coincidence must be in 0-1'
    # 如果键值对中的值大于或等于当前支持度阈值，则可以将该键值对作为频繁1-项集保留
    dic_1 = {}
    for item in dic:  # 如果对每一个议题的所选定的（y|n）进行计数，若计数总值超过了支持度所需要的计数，就把它放到下一个字典中
        if (dic[item] >= val_suport):
            dic_1[item] = dic[item]

    return dic_1


def mining_second(data, dic_before, support, confidence):
    '''
    进行关联规则的二次挖掘
    挖掘出候选2-项集

    注：所有挖掘出来的频繁项集都是以字典的形式存储的，字典的键是频繁项集，
    1频繁项集用1-16个整数，表示这些议题在原数据集中的下标；多频繁集就是这些下标的一个元组
    隐藏含义是这些议题共同被投票为vote_y_n，字典的值就是这样的组合出现的次数
    '''
    # 每一次扩展频繁项集的时候产生一个临时dict用于保存那些通过频繁项集生成算法可以留下的项集
    # 但是还要对其中的结果进行支持度判断，才能确定最终留下的算法
    dic = {}
    count = len(data)
    count2 = 0
    for data_line in data:
        # 获取元素数量
        count_item = len(data_line)
        # 每两个组合计数
        for i in range(0, count_item - 1):
            # 外层循环，控制频繁2-项集中的第一个元素的取值
            for j in range(i + 1, count_item):
                # 内层循环，控制频繁2-项集中的第二个元素的取值
                if (data_line[i] in dic_before and data_line[j] in dic_before):

                    count2 += 1
                    tmp = (data_line[i], data_line[j])
                    if (tmp in dic):
                        # 上同，使用键值对集合计数，只不过此时元素是二元的元组
                        dic[tmp] += 1
                    else:
                        dic[tmp] = 1
                else:
                    continue
                    # 当两个项中有一个不是频繁1-项集，根据剪枝策略，这样组成的项不是频繁2-项集
    # print(dic)
    assert (support >= 0) and (support <= 1), 'suport must be in 0-1'
    assert (confidence >= 0) and (confidence <= 1), 'confidence must be in 0-1'

    dic_2 = {}
    for item in dic:
        count_item0 = dic_before[item[0]]
        count_item1 = dic_before[item[1]]
        # 判断 支持度 和 置信度
        # 判断置信度的时候对于一个无序的元组，任何一种方向的规则都有可能，都要进行比较
        if ((dic[item] >= support * count) and (
                (dic[item] >= confidence * count_item0) or (dic[item] >= confidence * count_item1))):
            dic_2[item] = dic[item]

    return dic_2


def mining_third(data, dic_before, support, confidence):
    '''
    进行关联规则的三次挖掘
    挖掘出候选3-项集或者4-项集乃至n-项集
    '''
    # 频繁项集的产生使用Fk-1*Fk-1的策略
    dic_3 = {}
    for item0 in dic_before:
        # 外层循环控制频繁k-1项集中的某一项
        for item1 in dic_before:
            # 内层循环控制频繁k-1项集中的另一项
            if (item0 != item1):
                # print(item0,item1)
                item_len = len(item0)
                equal = True
                tmp_item3 = []
                # 判断前n-1项是否一致
                for i in range(item_len - 1):
                    tmp_item3.append(item0[i])
                    if (item0[i] != item1[i]):
                        equal = False
                        break
                if (equal == True):
                    # 如果两个Fk-1项具有k-2个公共前缀，那么就按照顺序，将其组合起来
                    minitem = min(item0[-1], item1[-1])
                    maxitem = max(item0[-1], item1[-1])
                    tmp_item3.append(minitem)
                    tmp_item3.append(maxitem)
                    tmp_item3 = tuple(tmp_item3)
                    dic_3[tmp_item3] = 0
                else:
                    continue
    # print('dic_3:',dic_3)
    # 暴力统计支持度的方法，对于每一个数据项，看每个新找到的k项集是否包含在数据项中
    # 比较的方法，是对项的每一位进行判断，看这一位是否在数据项中

    for data_line in data:
        for item in dic_3:
            is_in = True
            for i in range(len(item)):
                if (item[i] not in data_line):
                    is_in = False

            # 该候选k项集中的所有项都在数据项中，则可以将该项保留
            if (is_in == True):
                dic_3[item] += 1

    assert (support >= 0) and (support <= 1), 'suport must be in 0-1'
    assert (confidence >= 0) and (confidence <= 1), 'coincidence must be in 0-1'

    count = len(data)
    dic_3n = {}
    for item in dic_3:
        # 前一项的支持度计数，就是现在的项除去末尾的数字，通过键值对在原来的字典中查询的值
        count_item0 = dic_before[item[:-1]]
        # 判断 支持度 和 置信度
        if ((dic_3[item] >= support * count) and (dic_3[item] >= confidence * count_item0)):
            dic_3n[item] = dic_3[item]

    return dic_3n


def association_rules(freq_sets, min_conf):
    '''
    根据产生的频繁项集生成满足置信度要求的规则

    :param dict: 频繁项集的字典
    :param dict: 频繁项集字典中的频繁项集列表
    :param min_conf: 最小置信度
    :return: 规则列表
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

    # 支持度
    support = 0.3
    # 置信度
    confidence = 0.9

    # 总的y规则与两个党派的y规则
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

    # 总的n规则与两个党派的n规则
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