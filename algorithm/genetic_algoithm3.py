import copy
import pandas as pd
import re
import math
import itertools

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


'''主函数'''
if __name__ == '__main__':
    input_filename = 'E:/python/project/qasm/genetic_algoithm_test1.qasm'
    gate_list = converter_circuit_from_qasm(input_filename)[0]  # 门列表，表示所有门，控制位在前，目标为在后
    print(gate_list)
    gate_list = list_str_to_int(gate_list)
    print(gate_list)
    print(list_to_dag_list(gate_list))
