#遗传算法交换线序
# 2022.3.9
# 曹可欣
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
import datetime



Population_size = 20 # 种群大小
Mutation_rate = 0.001 # 变异概率
Crossover_rate = 0.8 # 交叉概率
N_generations = 20# 种群迭代次数


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


'''初始化种群'''
def initialize_population(line_sequence_combination):
    population_list = []
    for i in range(Population_size):
        line_dec = random.randint(0, len(line_sequence_combination)-1)
        population_list.append(line_sequence_combination[line_dec])
    return population_list


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


'''计算适应度 适应度函数使用的也是遗传算法'''
def fitness_function(gate_list,population,time_and_transmission_list,qbit):
    fitness_list = []
    for i in range(len(population)):
        fitness_list.append(single_fitness_function(gate_list,population[i],time_and_transmission_list,qbit))
    return fitness_list

'''计算单个适应度 适应度函数使用的也是遗传算法'''
def single_fitness_function(gate_list,line_sequence,time_and_transmission_list,qbit):
    initialize_line_sequence = line_sequence_change_combination(qbit)
    gate_list = fit.new_gate_list_by_line_sequence(gate_list,line_sequence,initialize_line_sequence)
    for i in range(len(gate_list)):
        global_gate_num = 0
        if len(gate_list[i]) == 2:
             if (gate_list[i][0] <= int(int(qbit) / 2)) & (gate_list[i][1] > int(int(qbit) / 2)):
                global_gate_num += 1
             if (gate_list[i][0] >= int(int(qbit) / 2)) & (gate_list[i][1] < int(int(qbit) / 2)):
                global_gate_num += 1
    fitness = len(gate_list) * 2 - global_gate_num
    return fitness


'''对种群列表按适应度排序'''
# def sort_population_list(population_list):
#    # print('排序前的'+str(len(population_list)))
#     for i in range(len(population_list)):
#         for j in range(0,len(population_list)-i-1):
#             if single_fitness_function(gate_list,population_list[j],time_and_transmission_list,qbit) >= single_fitness_function(gate_list,population_list[j+1],time_and_transmission_list,qbit):
#                 population_list[j],population_list[j+1] = population_list[j+1],population_list[j]
#   #  print(population_fitness(gate_list,population_list,time_and_transmission_list,qbit))
#   #  print('排序后的'+str(len(population_list)))
#     return population_list
def sort_population_list(population_list,fitness_list):
    for i in range(len(population_list)):
        for j in range(0, len(population_list) - i - 1):
            if fitness_list[j] <= fitness_list[j+1]:
                population_list[j], population_list[j + 1] = population_list[j + 1], population_list[j]
                fitness_list[j],fitness_list[j+1] = fitness_list[j+1],fitness_list[j]
    return population_list,fitness_list


'''选择 轮盘赌随机竞争'''
def select(fitness_list,population_list):
    # 总适应度
    fitness_sum = sum(fitness_list)
    selected_population_list = []
    # 每个染色体被选中的概率
    selected_probability_list = []
    for i in range(Population_size):
        selected_probability_i = (fitness_list[i]/fitness_sum)*100
        selected_probability_list.append(selected_probability_i)
    #print(selected_probability_list)
    k = 0
    match_fitness_list = []  # 对比list
    while k < Population_size:
        random_operator = random.randint(1, 99)  # 随机算子
        # if random_operator <= selected_probability_list[0]:
        #     match_fitness_list.append(0)
        for ki in range(Population_size):  # 60
            # 计算前q个和
            sum_front = 0
            sum_front_more = 0
            q = 0
            for q in range(ki):
                sum_front += selected_probability_list[q]
            sum_front_more = sum_front + selected_probability_list[q + 1]
            if (random_operator > sum_front) and (random_operator <= sum_front_more):
                match_fitness_list.append(q)
        k += 1
    #print(match_fitness_list)
    if len(match_fitness_list) < 10:
        for m in range(Population_size-len(match_fitness_list)):
            match_fitness_list.append(random.randint(0,Population_size-1))
    # 选取最好的一部分染色体
    sorted_population_list = sort_population_list(population_list,fitness_list)[0]
    print('排序后')
    print(sort_population_list(population_list,fitness_list)[1])
    print(sorted_population_list)
    print(fitness_function(gate_list,sorted_population_list,time_and_transmission_list,qbit))
    for best in range(int(len(population_list) * 1 / 5)):
        selected_population_list.append(sorted_population_list[best])
    # print(selected_probability_list)
    #  print(population_fitness(gate_list,selected_population_list,time_and_transmission_list,qbit))
    # 在match_fitness_list中对比适应度，留下高适应度的染色体  六条染色体只会留下三条 match_fitness_list[2,4,1,1,0,3]
    # p = 0
    # while p < len(match_fitness_list)-1:
    #     print(p)
    #     # selected_population_list.append(population_list[max(match_fitness_list[p],match_fitness_list[p+1])])
    #     if single_fitness_function(gate_list, population_list[match_fitness_list[p]], time_and_transmission_list, qbit) >= \
    #             single_fitness_function(gate_list, population_list[match_fitness_list[p + 1]], time_and_transmission_list,qbit):
    #         selected_population_list.append(population_list[match_fitness_list[p]])
    #         print('111111')
    #     if single_fitness_function(gate_list, population_list[match_fitness_list[p]], time_and_transmission_list, qbit) < \
    #             single_fitness_function(gate_list, population_list[match_fitness_list[p + 1]], time_and_transmission_list, qbit):
    #         selected_population_list.append(population_list[match_fitness_list[p + 1]])
    #         print('222222')
    #     p += 2

    # # 保留最优
    # max_fitness = max(fitness_list) # 最优适应度
    # selected_population_list.append(population_list[fitness_list.index(max_fitness)])
    # 随机竞争
    for p in range(0,len(match_fitness_list)-1,2):
        if fitness_list[match_fitness_list[p]]>=fitness_list[match_fitness_list[p+1]]:
            selected_population_list.append(population_list[match_fitness_list[p]])
        if fitness_list[match_fitness_list[p]]<fitness_list[match_fitness_list[p+1]]:
            selected_population_list.append(population_list[match_fitness_list[p+1]])
    return selected_population_list


'''交叉 3条染色体变道6个染色体'''
def crossover(selected_population_list):

    after_selected_population_list = copy.deepcopy(selected_population_list)
    new_population_list = []
    for father in selected_population_list:
        child = father
        if numpy.random.rand() < Crossover_rate:
            cross_pointa = random.randint(0,int(len(selected_population_list[0])/2)-1)
            cross_pointb = random.randint(int(len(selected_population_list[0] )/ 2),len(selected_population_list[0])-1)
            cross_point_contenta = child[cross_pointa]
            cross_point_contentb = child[cross_pointb]
            child = list(child)
            child[cross_pointa] = cross_point_contentb
            child[cross_pointb] = cross_point_contenta
            child = ''.join(child)
        # mutation(child)
        new_population_list.append(child)
    # del new_population_list[0]
    # new_population_list.extend(selected_population_list)
    difference = len(new_population_list)-(Population_size - len(selected_population_list))
    for i in range(difference):
        del new_population_list[random.randint(0,len(new_population_list)-1)]

    selected_population_list.extend(new_population_list)

    after_selected_population_list.extend(new_population_list)

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
    start_time = datetime.datetime.now()
    input_filename = 'E:/python/project/qasm/4gt5_76.qasm'
    gate_list = converter_circuit_from_qasm(input_filename)[0]
    gate_list = list_str_to_int(gate_list)
    print(gate_list)
    qbit = converter_circuit_from_qasm(input_filename)[1]
    # 生成执行时间和传输延时的模拟ist
    time_and_transmission_list = []
    for ti in range(len(gate_list)):
        time = [2, 5]
        time_and_transmission_list.append(time)
    line_combination = line_sequence_change_combination(qbit)
    print(line_combination)
    # 初始化种群
    population_list = initialize_population(line_combination)
    print(population_list)
    fitness_list = fitness_function(gate_list, population_list,time_and_transmission_list, qbit)
    print(fitness_list)
    # selected_population_list = select(fitness_list,population_list)
    # print(selected_population_list)
    # population_list = crossover(selected_population_list)
    # print(population_list)
    y_list = []  # 生成纵坐标
    for _ in range(N_generations):
        print('选择前')
        print(fitness_list)
        # 选择
        selected_population_list = select(fitness_list, population_list)
        y_list.append(mean(fitness_function(gate_list, selected_population_list, time_and_transmission_list, qbit)))
        print('选择后')
        print(fitness_function(gate_list, selected_population_list, time_and_transmission_list, qbit))
        # 交叉变异
        population_list = crossover(selected_population_list)
        # 计算种群的适应度函数
        fitness_list = fitness_function(gate_list, population_list, time_and_transmission_list, qbit)
        print('最终')
        print(fitness_list)
        print(' ')
        # y_list.append(mean(fitness_list))
    print(mean(fitness_list))

    end_time = datetime.datetime.now()
   # run_time = end_time-start_time

    print(end_time-start_time)
    # 画图
    # 生成横坐标
    x_list = []
    for x in range(N_generations):
        x_list.append(x)
    plt.plot(x_list,y_list)
    plt.show()