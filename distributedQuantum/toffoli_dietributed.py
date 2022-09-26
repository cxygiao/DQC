# toffoli门的隐形传态
# 2022.1.21
# cxy

import copy
import pandas as pd
import re
import math
from qiskit import QuantumCircuit
import itertools
import datetime

''' 流程
1.读取文件，将电路转换为gate_list [['0', '1', '9'], ['2', '9', '10'], ['1', '2', '9'], ['3', '10', '11'], ['3', '9', '10'], ['2', '3', '9'],
2.门的矩阵形式：[[1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1], 
3.交换线序，输出所有线序组合
4.在每种线序中，计算隐形传态次数
  4.1 隐形传态计算：寻找可以合并传输的门
5.求出最佳隐形传态次数以及线序

法一：# 是根据gate_list来判断是否为全局门，并非用materix_list
     # 交换线序后，直接改变gate_list，从而 materix_list也会改变
'''

def get_data(str):
    pattern = re.compile("[\d]+")
    result = re.findall(pattern, str)
    return result

'''
读取整个qasm文件
'''
def converter_circ_from_qasm(input_file_name):
 #   df_ori_qc = pd.DataFrame(columns=['k', 'c', 't'])  # 近邻化 以dataframe形式存储的近邻化量子电路
    gate_list =[]
    qbit = 0
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
            if line[0:2] == 'CX' or line[0:2] == 'cx':
                '''获取CNOT'''
                cnot = get_data(line)
                cnot_control = cnot[0]
                cnot_target = cnot[1]
                listSingle=[cnot_control,cnot_target]
                gate_list.append(listSingle)
            if line[0:3] == 'CCX' or line[0:3] == 'ccx':
                '''获取toffoli'''
                toffoli = get_data(line)
                toffoli_control1 = toffoli[0]
                toffoli_control2 = toffoli[1]
                toffoli_target = toffoli[2]
                listSingle = [toffoli_control1, toffoli_control2,toffoli_target]
                gate_list.append(listSingle)
    return gate_list, qbit


'''
将门转换为矩阵形式
'''
def gate_to_matrix(gate_list,qbit):
    matrix_list = []  # 矩阵list [[1,0,0,2,1] ,[1,2,0,0,0]]
    global_gate_sum = 0
    for s in range(len(gate_list)):
        qbit_sum_up = 0
        qbit_sum_down = 0
        matrix_son_list = [0] * (int(qbit)+1)
      #  matrix_son_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if len(gate_list[s]) == 2:  # cnot
            matrix_son_list[int(gate_list[s][0])] = 1
            matrix_son_list[int(gate_list[s][1])] = 2
        if len(gate_list[s]) == 3:   # toffoli
            matrix_son_list[int(gate_list[s][0])] = 1
            matrix_son_list[int(gate_list[s][1])] = 1
            matrix_son_list[int(gate_list[s][2])] = 2
        # matrix_list末尾元素为状态码，0：局部门，1：全局门
        for i in range(len(matrix_son_list)): # i：0-12
            if i < int((len(matrix_son_list)-1)/2):
                qbit_sum_up += matrix_son_list[i]
            else:
                qbit_sum_down += matrix_son_list[i]
        # 如果上半分区或下半分区的matrix_list全为0，既为局部门
        if qbit_sum_up == 0 or qbit_sum_down == 0:
            matrix_son_list[-1] = 0
        # 如果上半分区和下半分区的matrix_list都存在元素，既为全局门
        if qbit_sum_up != 0 and qbit_sum_down != 0:
            matrix_son_list[-1] = 1
        matrix_list.append(matrix_son_list)
        global_gate_sum += matrix_list[s][-1]
   # print('全局门个数：'+str(global_gate_sum))
    return matrix_list,global_gate_sum


'''toffoli门分解'''
def toffoli_decompose(gate_list):
    decompose_gate_list = []
    for i in range(len(gate_list)):
        if len(gate_list[i]) < 3: # 单量子门或者cnot门
            decompose_gate_list.append(gate_list[i])
        # toffoli 的两种分解方法
        if len(gate_list[i]) == 3: # toffoli门
            decompose_gate_list.append([gate_list[i][0], gate_list[i][2]])
            decompose_gate_list.append([gate_list[i][0], gate_list[i][1]])
            decompose_gate_list.append([gate_list[i][1], gate_list[i][2]])
            decompose_gate_list.append([gate_list[i][0], gate_list[i][1]])
            decompose_gate_list.append([gate_list[i][1], gate_list[i][2]])
        # if len(gate_list[i]) == 3: # toffoli门
        #     decompose_gate_list.append([gate_list[i][1], gate_list[i][2]])
        #     decompose_gate_list.append([gate_list[i][0], gate_list[i][1]])
        #     decompose_gate_list.append([gate_list[i][1], gate_list[i][2]])
        #     decompose_gate_list.append([gate_list[i][0], gate_list[i][1]])
        #     decompose_gate_list.append([gate_list[i][0], gate_list[i][2]])
    print(decompose_gate_list)
    return decompose_gate_list


'''反向电路'''
def reverse_circuit(gate_list):
    gate_list.reverse()
    return gate_list


'''
输出所有种线序组合
'''
def line_sequence_change_combination(qbit):
    str1 = ''
    # 最多支持 26量子位
    str2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
    for i in range(int(qbit)):
        # str1：ABCDEFGHIJKL.... 共qbit个
        str1 = str1 + str2[i]
    # 排列组合 将str1按qibt/2 一分为，共有C(qbit/2,qbit)种情况
    line_sequence_combination = []  # 线序排列集合['ABCDEF', 'ABCDEG', 'ABCDEH', 'ABCDEI', 'ABCDEJ', 'ABCDEK', 'ABCDEL', 'ABCDFG', 'ABCDFH', 'ABCDFI', 'ABCDFJ'......]
    for i in itertools.combinations(str1, int(int(qbit) / 2)):
        #  print(''.join(i), end=" ")
        line_sequence_combination.append(''.join(i))
    return line_sequence_combination


'''
把字母变成对于的数字
'''
def letter_to_number(letter):
    number = ord(letter) - 65
    return number


'''
将new_gate_list全部转换为int
'''
def list_str_to_int(gate_list):
    new_gate_list = []
    for i in range(len(gate_list)):
        son_new_gate_list = list(map(int,gate_list[i]))
        new_gate_list.append(son_new_gate_list)
    return new_gate_list


'''
根据前半部分线序推出全部线序  ABCDFG =>ABCDFGEHIJKL
'''
def single_to_all_line_sequence(line_sequence_combination,qbit):
    str2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
    all_line_sequence = list(line_sequence_combination)

    for i in range(int(qbit)):
        if str2[i] not in all_line_sequence:
            all_line_sequence.append(str2[i])
    new_all_line_sequence = "".join(all_line_sequence)

    return new_all_line_sequence


'''判断隐形传态方向，生成方向list'''
def judge_tc_direction(matrix_list):
    tc_direction_list = [-1] * len(matrix_list)  # 隐形传态方向
    # print(len(matrix_list))
    # print(tc_direction_list)
    for i in range(len(matrix_list)):
        matrix_list_element_sum_up = sum(matrix_list[i][0:int((len(matrix_list[i]) - 1) / 2)])  # 矩阵上半分区元素之和
        matrix_list_element_sum_down = sum(
            matrix_list[i][int((len(matrix_list[i]) - 1) / 2):int(len(matrix_list[i]) - 1)])  # 矩阵下半分区元素之和
       # print(str(i)+' '+str(matrix_list_element_sum_up)+' '+str(matrix_list_element_sum_down))
        if matrix_list[i][-1] == 1:
            # 判断传输方向
            if matrix_list_element_sum_up == matrix_list_element_sum_down:  # 都是2
                # 查找目标位在哪个分区
                for j in range(len(matrix_list[i]) - 1):
                    # 目标位在上
                    if matrix_list[i][j] == 2 and j < int((len(matrix_list[i]) - 1) / 2):
                        tc_direction_list[i] = 1
                    # 目标位在下
                    if matrix_list[i][j] == 2 and j >= int((len(matrix_list[i]) - 1) / 2):
                        tc_direction_list[i] = 0
            if matrix_list_element_sum_up == 1 and matrix_list_element_sum_down == 3:
                tc_direction_list[i] = 1
            if matrix_list_element_sum_up == 3 and matrix_list_element_sum_down == 1:
                tc_direction_list[i] = 0
    return tc_direction_list


'''删除不影响的局部门'''
def delete_useless_gate(matrix_list):
    i = 0
    while i < len(matrix_list)-1:
        matrix_list_element_sum_up = sum(matrix_list[i][0:int((len(matrix_list[i]) - 1) / 2)])  # 矩阵上半分区元素之和
        matrix_list_element_sum_down = sum(
            matrix_list[i][int((len(matrix_list[i]) - 1) / 2):int(len(matrix_list[i]) - 1)])
        # 一门是全局门，一门是局部门
        if matrix_list[i][-1] == 1 and matrix_list[i+1][-1] == 0:
            # 判断传输方向
            if matrix_list_element_sum_up == matrix_list_element_sum_down:  # 都是2
                # 查找目标位在哪个分区
                for j in range(len(matrix_list[i]) - 1):
                    # 目标位在上，向下传输
                    if matrix_list[i][j] == 2 and j < int((len(matrix_list[i]) - 1) / 2):
                        # 后一个门在下半分区，则可删除。既
                        if sum(matrix_list[i+1][0:int((len(matrix_list[i+1]) - 1) / 2)]) == 0:
                            del matrix_list[i+1]
                            i -= 1
                    # 目标位在下，向上传输
                    if matrix_list[i][j] == 2 and j >= int((len(matrix_list[i]) - 1) / 2):
                        if sum(matrix_list[i+1][int((len(matrix_list[i+1]) - 1) / 2):int(len(matrix_list[i+1]) - 1)]) == 0:
                            del matrix_list[i + 1]
                            i -= 1
            if matrix_list_element_sum_up == 1 and matrix_list_element_sum_down == 3:
                if sum(matrix_list[i+1][0:int((len(matrix_list[i+1]) - 1) / 2)]) == 0:
                    del matrix_list[i+1]
                    i -= 1
            if matrix_list_element_sum_up == 3 and matrix_list_element_sum_down == 1:
                if sum(matrix_list[i + 1][int((len(matrix_list[i + 1]) - 1) / 2):int(len(matrix_list[i + 1]) - 1)]) == 0:
                    del matrix_list[i + 1]
                    i -= 1

        i += 1

    return matrix_list


'''通过matrix_list变回gate_list [1, 0, 1, 2, 0, 0]=>[0,2,3]'''
def matrix_list_to_gate_list(matrix_list):
    gate_list = []
    for i in range(len(matrix_list)-1):
        if matrix_list[i] == 1:
            gate_list.append(i)
    for j in range(len(matrix_list)-1):
        if matrix_list[j] == 2:
            gate_list.append(j)
    return gate_list

'''相邻全局toffoli门的隐形传态'''
def toffoli_distributed(matrix_list,tc_direction_list,qbit):
    i = 0
    tc_num = 0 # 隐形传态次数
    t_target = 0
    for p in range(len(matrix_list)):
        if matrix_list[p][-1] == 1:
            tc_num += 1
   # print(tc_num)
    while i < len(matrix_list)-1:
        # 如果相邻两门都是全局门
        if matrix_list[i][-1] == 1 and matrix_list[i + 1][-1] == 1:

            '''如果两门都是toffoli门'''
            if sum(matrix_list[i]) == 5 and sum(matrix_list[i+1]) == 5:
                # 两toffoli门传输方向一致，且都是向下传输
                if tc_direction_list[i] == tc_direction_list[i+1] and tc_direction_list[i] == 1:
                    # 有相同的位，此时两门可以进行合并传输
                    for j1 in range(int((len(matrix_list[i]) - 1) / 2)):
                        # 两门具有相同位，且此时的量子位在上方分区
                        if (matrix_list[i][j1] == 1 and 1 == matrix_list[i + 1][j1]) or matrix_list[i][j1] + \
                                matrix_list[i + 1][j1] == 3 or (
                                matrix_list[i][j1] == 2 and 2 == matrix_list[i + 1][j1]):
                            # 满足以上所有推荐这两个门可以合并传输
                            tc_num -= 1  # 两门合并传输，计算隐形传态传输时，记载在后一个门
                            print('第' + str(i) + 'toffoli门向下合并传输一次')
                    # 跳出当前循环
                            break
                # 两toffoli门传输方向一致，且都是向上传输
                if tc_direction_list[i] == tc_direction_list[i + 1] and tc_direction_list[i] == 0:
                    for j2 in range(int((len(matrix_list[i]) - 1) / 2), len(matrix_list[i]) - 1):
                        if (matrix_list[i][j2] == 1 and 1 == matrix_list[i + 1][j2]) or matrix_list[i][j2] + \
                                matrix_list[i + 1][j2] == 3 or (
                                matrix_list[i][j2] == 2 and 2 == matrix_list[i + 1][j2]):
                            tc_num -= 1
                            print('第'+str(i)+'toffoli门向上合并传输一次')
                    # 跳出当前循环
                            break

            ''' 两个门都是cnot '''
            if sum(matrix_list[i]) == 4 and sum(matrix_list[i + 1]) == 4:
                    # 两集合有交集，则存在共同元素，可隐形传态
                same_qbit_list = list(set(matrix_list_to_gate_list(matrix_list[i])) & set(
                        matrix_list_to_gate_list(matrix_list[i + 1])))
                # 存在两相同量子位，则传输方向任意
                if len(same_qbit_list) == 2:
                    tc_num -= 1
                # 有一相同量子位，且在上半分区
                if len(same_qbit_list) == 1 and same_qbit_list[0] < int(int(qbit) / 2):
                    tc_direction = 1  # 此为i+1的传输方向
                    if tc_direction == tc_direction_list[i] or tc_direction_list[i] == -1:
                        tc_num -= 1
                        tc_direction_list[i + 1] = 1
                # 有一相同量子位，且在下半分区
                if len(same_qbit_list) == 1 and same_qbit_list[0] >= int(int(qbit) / 2):
                    tc_direction = 0  # 此为i+1的传输方向
                    if tc_direction == tc_direction_list[i] or tc_direction_list[i] == -1:
                        tc_num -= 1
                        tc_direction_list[i + 1] = 0

            '''一个是toffoli,一个是cnot'''
            if (sum(matrix_list[i]) == 5 and sum(matrix_list[i + 1]) == 4) :
                same_qbit_list = list(set(matrix_list_to_gate_list(matrix_list[i])) & set(
                    matrix_list_to_gate_list(matrix_list[i + 1])))
                # toffoli向下传输
                if tc_direction_list[i] == 1 :
                    for ci in range(int(len(matrix_list[i])-1)):
                        # 找toffoli目标位
                        if matrix_list[i][ci] == 2:
                            t_target = ci
                    # toffoli目标位在交集中，则可以合并传输
                    if t_target in same_qbit_list:
                        tc_direction_list[i+1] = 1
                        tc_num -= 1
                # toffoli向上传输
                if tc_direction_list[i] == 0:
                    for cj in range(len(matrix_list[i])-1):
                        # 找toffoli目标位
                        if matrix_list[i][cj] == 2:
                            t_target = cj
                    # toffoli目标位在交集中，则可以合并传输
                    if t_target in same_qbit_list:
                        tc_direction_list[i + 1] = 0
                        tc_num -= 1
             # 一个是toffoli,一个是cnot
            if (sum(matrix_list[i]) == 4 and sum(matrix_list[i + 1]) == 5):
                same_qbit_list = list(set(matrix_list_to_gate_list(matrix_list[i])) & set(
                    matrix_list_to_gate_list(matrix_list[i + 1])))
                # toffoli向下传输
                if tc_direction_list[i+1] == 1 and tc_direction_list[i] != 0:
                    for ci in range(int(len(matrix_list[i+1]) - 1)):
                        # 找toffoli目标位
                        if matrix_list[i+1][ci] == 2:
                            t_target = ci
                    # toffoli目标位在交集中，则可以合并传输
                    if t_target in same_qbit_list:
                        tc_direction_list[i] = 1
                        tc_num -= 1
                # toffoli向上传输
                if tc_direction_list[i+1] == 0 and tc_direction_list[i] != 1:
                    for cj in range(len(matrix_list[i+1]) - 1):
                         # 找toffoli目标位
                        if matrix_list[i+1][cj] == 2:
                            t_target = cj
                    # toffoli目标位在交集中，则可以合并传输
                    if t_target in same_qbit_list:
                        tc_direction_list[i] = 0
                        tc_num -= 1

        i += 1
    return matrix_list,tc_num


'''
主函数
'''
if __name__ == '__main__':
    start_time = datetime.datetime.now()
    input_filename = 'E:/python/project/qasm/sym9_147_swap4.qasm'
   # gate_list = converter_circ_from_qasm(input_filename)[0]
    qbit = converter_circ_from_qasm(input_filename)[1]        # 量子位
    print(converter_circ_from_qasm(input_filename)[0])
    gate_list = converter_circ_from_qasm(input_filename)[0]
   #  # toffoli分解
   #  gate_list = toffoli_decompose(converter_circ_from_qasm(input_filename)[0])
   #  print(gate_list)
   #  # 反向电路
   #  gate_list = reverse_circuit(gate_list)
   #  print(gate_list)
    # print(len(gate_list))      # 门
    # matrix_list = gate_to_matrix(gate_list,qbit)
    # print(matrix_list)   # 矩阵形式
    #gate_list = toffoli_decompose(gate_list)
    # 是根据gate_list来判断是否为全局门，并非用matrix_list
    # 直接改变gate_list，从而 matrix_list也会改变
    #  new_gate_list = []  # 改变线序后的gate_list
    line_sequence_combination = line_sequence_change_combination(qbit)
    print(line_sequence_combination)  # 输出所有种线序组合
    initial_line_sequence = single_to_all_line_sequence(line_sequence_combination[0],qbit)  #ABCDEF GHIJKL
    print(initial_line_sequence)

    min_tc = len(gate_list)  # 最小隐形传态次数(全局门合并)
    min_line_sequence = ''
    # 根据线序改变gate_list
    for i in range(len(line_sequence_combination)):  # i: 0-923
        new_gate_list = list_str_to_int(gate_list)
        all_line_sequence = single_to_all_line_sequence(line_sequence_combination[i],qbit)   # ABCDEG FHIJKL
        for j in range(len(all_line_sequence)):  # j: 0-11
            if all_line_sequence[j] == initial_line_sequence[j]:
                continue
            if all_line_sequence[j] != initial_line_sequence[j]:
                for k in range(len(new_gate_list)):  # k: 门数
                    for p in range(len(new_gate_list[k])):  # l:0-3
                        if new_gate_list[k][p] == letter_to_number(all_line_sequence[j]):
                            new_gate_list[k][p] = str(j)
        print(list_str_to_int(new_gate_list))

        matrix_list = gate_to_matrix(new_gate_list, qbit)[0]
        global_gate_num = gate_to_matrix(new_gate_list, qbit)[1] # 统计全局门个数
        print(global_gate_num)
        toffoli_list = delete_useless_gate(matrix_list)
       # print(matrix_list)
        # 输出模块
        print(all_line_sequence)
        toffoli_result_list = toffoli_distributed(toffoli_list,judge_tc_direction(toffoli_list),qbit)
        print('相邻的全局toffoli门的隐形传态次数：'+str(toffoli_result_list[1]))
        if toffoli_result_list[1] < min_tc:
            min_gate_list = new_gate_list
            min_tc = toffoli_result_list[1]
            min_line_sequence = all_line_sequence
            min_global_gate_num = global_gate_num
            min_matrix_list = matrix_list
        print(' ')
    end_time = datetime.datetime.now()


print('################################################')
print(min_matrix_list)
print(list_str_to_int(min_gate_list))
print(len(min_matrix_list))
print('toffoli合并最小隐形传态次数（分解）:'+str(min_tc))
print('此时线序：'+str(min_line_sequence)+ ' '+'全局门个数:'+str(min_global_gate_num))
print('################################################')
print(end_time - start_time)

# # 绘图
# circ = QuantumCircuit(int(qbit),int(len(gate_list)))
# for y in range(len(min_gate_list)):
#     circ.cx(int(min_gate_list[y][0]),int(min_gate_list[y][1]))
# print(circ)

