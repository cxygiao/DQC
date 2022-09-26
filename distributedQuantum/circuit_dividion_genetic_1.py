#遗传算法线路划分
# vision 2.0 在初始化种群时，直接随机生成线序，不在生成的所有线序中选择出初始种群
# 2022.7.9
# 陈新宇
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
import distributedQuantum.distributed_genctic as dg

Population_size = 20  # 种群大小
Mutation_rate = 0.001  # 变异概率
Crossover_rate = 0.8  # 交叉概率
N_generations = 50  # 种群迭代次数

'''读取qasm文件并进行存储'''
def converter_circ_from_qasm(input_file_name):
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
            if line[0:2] == 'cr':

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
            if line[0:2] == 'CP' or line[0:2] == 'cp':
                cp = get_data(line)
                cp_one = cp[1]
                cp_two = cp[2]
                listSingle = [cp_one,cp_two]
                gate_list.append(listSingle)
            if line[0:4] == 'SWAP' or line[0:4] == 'swap':
                swap = get_data(line)
                swap_one = swap[0]
                swap_two = swap[1]
                cnot_one = [swap_one,swap_two]
                cnot_two = [swap_two,swap_one]
                gate_list.append(cnot_one)
                gate_list.append(cnot_two)
                gate_list.append(cnot_one)
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

# '''
# 输出所有种线序组合
# '''
# def line_sequence_change_combination(qbit):
#     str1 = ''
#     final_line_sequence_combination = []
#     # 最多支持 26量子位
#     str2 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A',
#             'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
#             'V', 'W', 'X', 'Y', 'Z']
#     for i in range(int(qbit)):
#         # str1：ABCDEFGHIJKL.... 共qbit个
#         str1 = str1 + str2[i]
#     # 排列组合 将str1按qibt/2 一分为，共有C(qbit/2,qbit)种情况
#     line_sequence_combination = []  # 线序排列集合['ABCDEF', 'ABCDEG', 'ABCDEH', 'ABCDEI', 'ABCDEJ', 'ABCDEK', 'ABCDEL', 'ABCDFG', 'ABCDFH', 'ABCDFI', 'ABCDFJ'......]
#     for i in itertools.combinations(str1, int(int(qbit) / 2)):
#         #  print(''.join(i), end=" ")
#         line_sequence_combination.append(''.join(i))
#     for j in range(len(line_sequence_combination)):
#         final_line_sequence_combination.append(single_to_all_line_sequence(line_sequence_combination[j], qbit))
#     return final_line_sequence_combination
#
#
# '''根据前半部分线序推出全部线序  ABCDFG =>ABCDFGEHIJKL'''
# def single_to_all_line_sequence(line_sequence_combination,qbit):
#     # str2 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#     str2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
#             'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
#             'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
#     all_line_sequence = list(line_sequence_combination)
#
#     for i in range(int(qbit)):
#         if str2[i] not in all_line_sequence:
#             all_line_sequence.append(str2[i])
#     new_all_line_sequence = "".join(all_line_sequence)
#     return new_all_line_sequence

# 生成初始线序 返回10个随机的初始线序
def generate_line_sequence(qbit):
    initial_line_sequence = []
    qbit = int(qbit)
    str1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9','!','@']
    # 首位线序 abcdefg...
    single_line_sequence = str1[:qbit]
    # 生成十个随机的初始线序
    for i in range(Population_size):
        random.shuffle(single_line_sequence)
        initial_line_sequence.append(''.join(single_line_sequence))
    return initial_line_sequence

# 生成原始线序 abcdefg
def generate_initial_line_sequence(qbit):
    qbit = int(qbit)
    str1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9','!','@']
    # 首位线序 abcdefg...
    line_sequence = str1[:qbit]
    initial_line_sequence = ''.join(line_sequence)
    return initial_line_sequence


'''把字母变成对于的数字'''
def letter_to_number(letter):
    number = ord(letter) - 65
    return number


'''初始化种群'''
def initialize_population(qbit):
    population_list = generate_line_sequence(qbit)
    return population_list


'''种群适应度函数list'''
def population_fitness_list(gate_list,population_list,initial_line_sequence,qbit):
    fitness_list = []
    for i in range(len(population_list)):
        fitness_list.append(dg.tc_num_by_merge(gate_list,population_list[i],initial_line_sequence,qbit))
    return fitness_list


'''某条染色体的适应度'''
def single_fitness(gate_list,line_sequence,initial_line_sequence,qbit):
    fitness = dg.tc_num_by_merge(gate_list,line_sequence,initial_line_sequence,qbit)
    return fitness


'''对种群列表按适应度排序'''
def sort_population_list(population_list,fitness_list):
    for i in range(len(population_list)):
        for j in range(0, len(population_list) - i - 1):
            if fitness_list[j] >= fitness_list[j+1]:
                population_list[j], population_list[j + 1] = population_list[j + 1], population_list[j]
                fitness_list[j],fitness_list[j+1] = fitness_list[j+1],fitness_list[j]
    return population_list,fitness_list


'''
选择 最佳保留+随机竞争
选择过后，种群只会保留一半
'''
def select(population_list,fitness_list,initial_line_sequence,qbit):
    selected_population_list = []
    # 保留最佳染色体
    selected_population_list.append(sort_population_list(population_list,fitness_list)[0][0])
    # 随机竞争
    for i in range(int(len(population_list)/2)):
        random_operator1 = random.randint(0,len(population_list)-1)  # 随机算子
        random_operator2 = random.randint(0,len(population_list)-1)
        if single_fitness(gate_list,population_list[random_operator1],initial_line_sequence,qbit) <= single_fitness(gate_list,population_list[random_operator2],initial_line_sequence,qbit):
            selected_population_list.append(population_list[random_operator1])
        if single_fitness(gate_list, population_list[random_operator1], initial_line_sequence, qbit) > single_fitness(
                gate_list, population_list[random_operator2], initial_line_sequence, qbit):
            selected_population_list.append(population_list[random_operator2])
    return selected_population_list


'''交叉 '''
def crossover(selected_population_list):
    after_selected_population_list = copy.deepcopy(selected_population_list)
    new_population_list = []
    for father in selected_population_list:
        child = father
        if numpy.random.rand() < Crossover_rate:
            cross_pointa = random.randint(0,int(len(selected_population_list[0])/2)-1)
            cross_pointb = random.randint(int(len(selected_population_list[0])/ 2),len(selected_population_list[0])-1)
            cross_point_contenta = child[cross_pointa]
            cross_point_contentb = child[cross_pointb]
            child = list(child)
            child[cross_pointa] = cross_point_contentb
            child[cross_pointb] = cross_point_contenta
            child = ''.join(child)
        # mutation(child)
        new_population_list.append(child)
    difference = len(new_population_list)-(Population_size - len(selected_population_list))
    for i in range(difference):
        del new_population_list[random.randint(0,len(new_population_list)-1)]
    selected_population_list.extend(new_population_list)
    after_selected_population_list.extend(new_population_list)
    return after_selected_population_list


'''主函数'''
if __name__ == '__main__':
    start_time = datetime.datetime.now()
    input_filename = 'E:/python/project/qasm/4gt5_75.qasm'
    # gate_list = converter_circ_from_qasm(input_filename)[0]
    qbit = converter_circ_from_qasm(input_filename)[1]  # 量子位
    print('量子位数：'+str(qbit))
    gate_list = list_str_to_int(converter_circ_from_qasm(input_filename)[0])
    print('qasm读取线路:',end=' ')
    print(gate_list)
    # 线序组合
    # line_sequence_combination = line_sequence_change_combination(qbit)
    # initial_line_sequence = line_sequence_combination[0]
    # print('初始线序组合'+str(line_sequence_combination))
    initial_line_sequence = generate_initial_line_sequence(qbit)
    print('初始化种群：',end='')
    population_list = initialize_population(qbit)
    print(population_list)
    fitness_list = population_fitness_list(gate_list,population_list,initial_line_sequence,qbit)
    print('初始适应度：', end='')
    print(fitness_list)
    # print(sort_population_list(population_list,fitness_list))
    # population_list = select(population_list,fitness_list,initial_line_sequence,qbit)
    # print(population_list)

    # 遗传算法迭代
    for _ in range(N_generations):
        # 选择
        selected_population_list = select(population_list,fitness_list,initial_line_sequence,qbit)
        # 交叉变异
        population_list = crossover(selected_population_list)
        # 计算种群的适应度函数
        fitness_list = population_fitness_list(gate_list,population_list,initial_line_sequence,qbit)
    end_time = datetime.datetime.now()
    # 输出模块
    print('##########################################################################################################')
    print('最佳隐形传态次数：', end='')
    print(min(fitness_list))
    print('程序执行时间：', end='')
    print(end_time - start_time)
    print(population_list)

    print(fitness_list)
    print('##########################################################################################################')