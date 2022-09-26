import copy
from audioop import avg

import pandas as pd
import re
import math
import itertools
import random
import numpy
import matplotlib.pyplot as plt
from numpy.core import mean

Population_size = 20  # 种群大小
Mutation_rate = 0.001 # 变异概率
Crossover_rate = 0.8 # 交叉概率
N_generations = 200 # 种群迭代次数

'''读取qasm文件并进行存储'''
def converter_circuit_from_qasm(input_file_name):
    gate_list = []
    qbit = 0  # 量子位
    qasm_file = open(input_file_name, 'r')
    iter_f = iter(qasm_file)
    reserve_line = 4
    num_line = 0
    for line in iter_f:  # 遍历文件，一行行遍历，读取文本
        num_line += 1
        if num_line <= reserve_line:
            continue
        else:
            if line[0:4] == 'creg':
                qbit = get_data(line)[0]
            if line[0:1] == 'x' or line[0:1] == 'X':
                '''获取X门'''
                x = get_data(line)
                x_target = x[0]
                listSingle = [x_target]
                gate_list.append(listSingle)
            if line[0:2] == 'CX' or line[0:2] == 'cx':
                '''获取CNOT'''
                cnot = get_data(line)
                cnot_control = cnot[0]
                cnot_target = cnot[1]
                listSingle = [cnot_control, cnot_target]
                gate_list.append(listSingle)
            if line[0:3] == 'CCX' or line[0:3] == 'ccx':
                '''获取toffoli'''
                toffoli = get_data(line)
                toffoli_control1 = toffoli[0]
                toffoli_control2 = toffoli[1]
                toffoli_target = toffoli[2]
                listSingle = [toffoli_control1, toffoli_control2, toffoli_target]
                gate_list.append(listSingle)
    return gate_list, qbit


def get_data(str):
    pattern = re.compile("[\d]+")
    result = re.findall(pattern, str)
    return result

'''
将new_gate_list全部转换为int
'''
def list_str_to_int(gate_list):
    new_gate_list = []
    for i in range(len(gate_list)):
        son_new_gate_list = list(map(int, gate_list[i]))
        new_gate_list.append(son_new_gate_list)
    return new_gate_list


'''把gate_lsit转化为dag图，返回list'''
def list_to_dag_list(gate_list):
    dag_list = copy.deepcopy(gate_list)
    dag_list[0].append('-1')  # 前驱-1即无前驱
    for i in range(1, len(gate_list)):
        j = i - 1
        if len(list(set(gate_list[i]) & set(gate_list[j]))) > 0:  # 两个集合有交集，则表示有前驱后驱关系，即dag图上有箭头
            dag_list[i].append(str(j))
        if len(list(set(gate_list[i]) & set(gate_list[j]))) == 0:  # 两集合无交集，没有依赖关系
            dag_list[i].append('-1')
            while j >= 0:
                if len(list(set(gate_list[i]) & set(gate_list[j - 1]))) == 0:
                    j -= 1
                    continue
                if len(list(set(gate_list[i]) & set(gate_list[j - 1]))) > 0:
                    dag_list[i][-1] = str(j - 1)
                    break
    return dag_list


'''生成类似时间表这么一个玩意,把可以并行执行的门，放到同一个gatelist里'''
def time_table(gate_list):
    more_gate_list = []
    i = 0
    while i < len(gate_list) -1:
        j = i + 1
        for j in range(len(gate_list)):
            if max(gate_list[j]) < min(gate_list[i]):
                more_gate_list.append()



'''输出所有线序组合'''
def line_sequence_change_combination(qbit):
    # 字母计数法 最多支持26量子位
    str1 = ''
    str2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
    for i in range(int(qbit)):
        str1 = str1 + str2[i]
    # 排列组合 将str1按qbit分成A(qbit,qbit)情况
    line_sequence_combination = []  # 线序排列集合['ABCDEF','ABCDEG','',....'']
    for j in itertools.permutations(str1, int(qbit)):
        line_sequence_combination.append(''.join(j))
    return line_sequence_combination


'''
把字母变成对于的数字
'''
def letter_to_number(letter):
    number = ord(letter) - 65
    return number


'''染色体编码 01编码方式'''
def chromosome_coding(gate_num):
    # gate_num转化为二进制计算
    code_max = 2 ** gate_num
    code_dec = random.randint(0, code_max)
    chromosome_coding_number = bin(code_dec)
    chromosome_coding_list = list(str(chromosome_coding_number))
    del chromosome_coding_list[0:2]
    # 补齐染色图到八位
    if len(chromosome_coding_list) < gate_num:
        for i in range(gate_num - len(chromosome_coding_list)):
            chromosome_coding_list.insert(0, '0')
    return chromosome_coding_list


'''初始化种群'''
def initialize_population(gate_num):
    population_list = []
    for i in range(Population_size):
        population_list.append(chromosome_coding(gate_num))
    population_list = list_str_to_int(population_list)
    return population_list


'''适应度函数，即电路执行总时间（包括门执行时机和通信延迟）'''
def fitness_function(gate_list, chromosome_coding_list, time_and_transmission_list, qbit):
    total_circuit_operation_time = 0
    teleportation_num = 0
    # 先计算传输时间
    for i in range(len(gate_list)):
        # 判断是否需要加上传输时间
        gate_partition = []
        for j in range(len(gate_list[i])):
            # 在上半分区
            if gate_list[i][j] < int(int(qbit) / 2):
                gate_partition.append(0)
            if gate_list[i][j] >= int(int(qbit) / 2):
                gate_partition.append(1)

        # 此门在上半分区
        if sum(gate_partition) == 0:
            # if chromosome_coding_list[i] == 0:
            #     total_circuit_operation_time = total_circuit_operation_time
            if chromosome_coding_list[i] == 1:
                total_circuit_operation_time += time_and_transmission_list[i][1]
                if len(gate_partition) == 1: # 单量子门
                    teleportation_num += 1
                if len(gate_partition) == 2: # 双量子门
                    teleportation_num += 2
        # 此门在下半分区
        if (sum(gate_partition) == 2 and len(gate_partition) == 2) or (
                sum(gate_partition) == 1 and len(gate_partition) == 1):

            if chromosome_coding_list[i] == 0:
                total_circuit_operation_time += time_and_transmission_list[i][1]
                if len(gate_partition) == 1:  # 单量子门
                    teleportation_num += 1
                if len(gate_partition) == 2:  # 双量子门
                    teleportation_num += 2
            # if chromosome_coding_list[i] == 1:
            #     total_circuit_operation_time = total_circuit_operation_time
        # 横跨两个区
        if sum(gate_partition) == 1 and len(gate_partition) == 2:
            teleportation_num += 1
            total_circuit_operation_time += time_and_transmission_list[i][1]

    # 适应度 = 总门数 - 需要传输的量子位的数量
    fitness = len(gate_list)*2 - teleportation_num
    # 适应度 2= 总隐形传态时间 - 隐形传态时间
    sum_tc = len(gate_list)*5
    # for k in range(len(time_and_transmission_list)):
    #     sum_tc += time_and_transmission_list[k][1]
    # fitness = sum_tc + 1 - total_circuit_operation_time
    return total_circuit_operation_time,fitness


'''依据适应度函数和种群，生成种群的适应度list'''
def population_fitness(gate_list, population_list, time_and_transmission_list, qbit):
    fitness_list = []
    for i in range(len(population_list)): # 0-5
        fitness_list.append(fitness_function(gate_list,population_list[i],time_and_transmission_list, qbit)[1])
    return fitness_list

'''依据适应度函数和种群，生成种群的代价函数时间list'''
def population_time(gate_list, population_list, time_and_transmission_list, qbit):
    tc_time_list = []
    for i in range(Population_size): # 0-5
        tc_time_list.append(fitness_function(gate_list,population_list[i],time_and_transmission_list, qbit)[0])
    return tc_time_list


'''对种群列表按适应度排序'''
def sort_population_list(population_list):
   # print('排序前的'+str(len(population_list)))
    for i in range(len(population_list)):
        for j in range(0,len(population_list)-i-1):
            if fitness_function(gate_list,population_list[j],time_and_transmission_list,qbit) >= fitness_function(gate_list,population_list[j+1],time_and_transmission_list,qbit):
                population_list[j],population_list[j+1] = population_list[j+1],population_list[j]
  #  print(population_fitness(gate_list,population_list,time_and_transmission_list,qbit))
  #  print('排序后的'+str(len(population_list)))
    return population_list


'''选择 轮盘赌+随机竞争'''
def select(fitness_list,population_list):
    # 总适应度
    fitness_sum = sum(fitness_list)
    selected_population_list = []
    # 每个染色体被选中的概率
    selected_probability_list = []
    for i in range(Population_size):
        selected_probability_i = (fitness_list[i]/fitness_sum)*100
        selected_probability_list.append(selected_probability_i)
    # print(selected_probability_list)
   #  模拟轮盘选择 选择策略：保留最优，再两两随机竞争
   #  min_fitness_list = fitness_list[0]
   #  max_fitness_list = fitness_list[0]
   #  max_fitness_list_i = 0
   #  for j in range(Population_size):
   #      if fitness_list[j] > max_fitness_list:
   #          max_fitness_list = fitness_list[j]
   #          max_fitness_list_i = j
   #      if fitness_list[j] < min_fitness_list:
   #          min_fitness_list = fitness_list[j]
   #          min_fitness_list_i = j
   #  selected_population_list.append(population_list[max_fitness_list_i])  # 保留最优

    # 两两随机竞争
    # while k < Population_size:
    #     random_operator = random.randint(1,99)  # 随机算子
    #     # print(random_operator)
    #     if random_operator <= selected_probability_list[0]:
    #         match_fitness_list.append(0)
    #     if (random_operator > selected_probability_list[0]) and (random_operator <= (selected_probability_list[0]+selected_probability_list[1])):
    #         match_fitness_list.append(1)
    #     if (random_operator > (selected_probability_list[0]+selected_probability_list[1])) and (random_operator <= (selected_probability_list[0] + selected_probability_list[1] + selected_probability_list[2])):
    #         match_fitness_list.append(2)
    #     if (random_operator > (selected_probability_list[0] + selected_probability_list[1] + selected_probability_list[2])) and (random_operator <= (selected_probability_list[0] + selected_probability_list[1] + selected_probability_list[2] + selected_probability_list[3])):
    #         match_fitness_list.append(3)
    #     if (random_operator > (selected_probability_list[0] + selected_probability_list[1] + selected_probability_list[2] + selected_probability_list[3])) and (random_operator <= (selected_probability_list[0] + selected_probability_list[1] + selected_probability_list[2] + selected_probability_list[3] + selected_probability_list[4])):
    #         match_fitness_list.append(4)
    #     if (random_operator > (selected_probability_list[0] + selected_probability_list[1] + selected_probability_list[2] + selected_probability_list[3] + selected_probability_list[4])) and (random_operator <= sum(selected_probability_list)):
    #         match_fitness_list.append(5)
    #     k += 1
    k = 0
    match_fitness_list = []  # 对比list
    while k < Population_size:
        random_operator = random.randint(1,99)  # 随机算子
        if random_operator <= selected_probability_list[0]:
             match_fitness_list.append(0)
        for ki in range(Population_size): # 60
            # 计算前q个和
            sum_front = 0
            q = 0
            for q in range(ki):
                sum_front += selected_probability_list[q]
            sum_front_more = sum_front + selected_probability_list[q+1]
            if (random_operator > sum_front) and (random_operator <= sum_front_more):
                match_fitness_list.append(q)
        k += 1

    # 选取最好的一部分染色体
    for best in range(int(len(population_list)*1/5)):
        selected_population_list.append(sort_population_list(population_list)[best])

  #  print(population_fitness(gate_list,selected_population_list,time_and_transmission_list,qbit))
    # 在match_fitness_list中对比适应度，留下高适应度的染色体  六条染色体只会留下三条 match_fitness_list[2,4,1,1,0,3]
    p = 0
    while p < Population_size:
        # selected_population_list.append(population_list[max(match_fitness_list[p],match_fitness_list[p+1])])
        if fitness_function(gate_list, population_list[match_fitness_list[p]], time_and_transmission_list, qbit)[1] >= fitness_function(gate_list,population_list[match_fitness_list[p+1]],time_and_transmission_list,qbit)[1] :
            selected_population_list.append(population_list[match_fitness_list[p]])
        if fitness_function(gate_list, population_list[match_fitness_list[p]], time_and_transmission_list, qbit)[1]  < fitness_function(
                gate_list, population_list[match_fitness_list[p+1]], time_and_transmission_list, qbit)[1] :
            selected_population_list.append(population_list[match_fitness_list[p+1]])
        p += 2

    # print('选择时')
    # print(population_fitness(gate_list, selected_population_list, time_and_transmission_list, qbit))
    return selected_population_list


'''交叉 3条染色体变道6个染色体'''
'''问题出在这，不能3=>6 应该是4=>6'''
def crossover(selected_population_list):
    # print('交叉时')
    # print(population_fitness(gate_list, selected_population_list, time_and_transmission_list, qbit))
    after_selected_population_list = copy.deepcopy(selected_population_list)
    new_population_list = []
    for father in selected_population_list:
        child = father
        if numpy.random.rand() < Crossover_rate:
            mother = selected_population_list[random.randint(0,len(selected_population_list))-1]
            cross_points = random.randint(0,len(gate_list)-1)
            child[cross_points:] = mother[cross_points:]
        mutation(child)
        new_population_list.append(child)
    # del new_population_list[0]
    # new_population_list.extend(selected_population_list)

    # print(population_fitness(gate_list, new_population_list, time_and_transmission_list, qbit))
    # # 保留最优子代
    # selected_population_list.append(sort_population_list(new_population_list)[0])

    # 对new_population_list选择
    difference = len(new_population_list)-(Population_size - len(selected_population_list))
    for i in range(difference):
        del new_population_list[random.randint(0,len(new_population_list)-1)]
   # print(population_fitness(gate_list, new_population_list, time_and_transmission_list, qbit))
    selected_population_list.extend(new_population_list)

    after_selected_population_list.extend(new_population_list)
    # print('交叉后')
    # print(population_fitness(gate_list, after_selected_population_list, time_and_transmission_list, qbit))

    return after_selected_population_list


'''变异'''
def mutation(child):
    # 变异的概率很低
    if numpy.random.rand() == Mutation_rate:
        mutate_point = random.randint(0, len(child)-1)
        child[mutate_point] = child[mutate_point] ^ 1
        print('变异一次')
    return child




'''主函数'''
if __name__ == '__main__':
    input_filename = 'E:/python/project/qasm/min-alu-305.qasm'
    gate_list = converter_circuit_from_qasm(input_filename)[0]  # 门列表，表示所有门，控制位在前，目标为在后
    print(gate_list)
    gate_list = list_str_to_int(gate_list)
    print(gate_list)
    # 生成执行时间和传输延时的模拟ist
    time_and_transmission_list = []
    for ti in range(len(gate_list)):
        time = [2,5]
        time_and_transmission_list.append(time)
    print(time_and_transmission_list)
    print('gate_list长度'+str(len(gate_list)))
    print(list_to_dag_list(gate_list))
    qbit = converter_circuit_from_qasm(input_filename)[1]
#    print(line_sequence_change_combination(qbit))
    initial_line_sequence = line_sequence_change_combination(qbit)[0]  # 初始线序 ABCDEF
    avg_fitness_list = []
   # 交换线序 改变的是gate_list
    for i in range(len(line_sequence_change_combination(qbit))):
        int_gate_list = list_str_to_int(gate_list)
        all_line_sequence = line_sequence_change_combination(qbit)[i]

        for j in range(len(all_line_sequence)):
            if all_line_sequence[j] == initial_line_sequence[j]:
                continue
            if all_line_sequence[j] != initial_line_sequence[j]:
                for k in range(len(int_gate_list)):  # k: 门数
                    for p in range(len(int_gate_list[k])):
                        if int_gate_list[k][p] == letter_to_number(all_line_sequence[j]):
                            int_gate_list[k][p] = str(j)
        print(all_line_sequence)
      #  print(list_str_to_int(int_gate_list))
        gate_list = list_str_to_int(int_gate_list)
      #  print(gate_list)
        ###############################################
        # 下面开始遗传算法
        # 初始化种群
        population_list = initialize_population(len(gate_list))
        # print(population_list)
        fitness_list = population_fitness(gate_list, population_list, time_and_transmission_list, qbit)
        for _ in range(N_generations):
            # 选择
            selected_population_list = select(fitness_list, population_list)
            # 交叉变异
            population_list = crossover(selected_population_list)
            # 计算种群的适应度函数
            fitness_list = population_fitness(gate_list, population_list, time_and_transmission_list, qbit)
        avg_fitness_list.append(mean(population_fitness(gate_list, population_list, time_and_transmission_list, qbit)))
        print(mean(population_fitness(gate_list, population_list, time_and_transmission_list, qbit)))

    print(avg_fitness_list)
    print(max(avg_fitness_list))