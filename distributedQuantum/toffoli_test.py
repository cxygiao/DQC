import copy
import pandas as  pd
import re
import math
import itertools

'''toffoli门分解'''
def toffoli_decompose(gate_list):
    decompose_gate_list = []
    for i in range(len(gate_list)):
        if len(gate_list[i]) < 3: # 单量子门或者cnot门
            decompose_gate_list.append(gate_list[i])
        if len(gate_list[i]) == 3: # toffoli门
            decompose_gate_list.append([gate_list[i][0], gate_list[i][2]])
            decompose_gate_list.append([gate_list[i][0], gate_list[i][1]])
            decompose_gate_list.append([gate_list[i][1], gate_list[i][2]])
            decompose_gate_list.append([gate_list[i][0], gate_list[i][1]])
            decompose_gate_list.append([gate_list[i][1], gate_list[i][2]])
    return decompose_gate_list

'''判断隐形传态方向，生成方向list 0向上传输 1向下传输 -1待定传输方向'''
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
    t_target = 0
    tc_num = 0 # 隐形传态次数
    for p in range(len(matrix_list)):
        if matrix_list[p][-1] == 1:
            tc_num += 1
    print(tc_num)
    while i < len(matrix_list)-1:
        # # 全局门后跟着一个局部门，则这个门单独隐形传态
        # if matrix_list[i][-1] == 1 and matrix_list[i + 1][-1] == 0:
        #     tc_num += 1
        # 如果相邻两门都是全局门
        if matrix_list[i][-1] == 1 and matrix_list[i + 1][-1] == 1:
            # 如果两门都是toffoli门
            if sum(matrix_list[i]) == 5 and sum(matrix_list[i+1]) == 5:
                # 两toffoli门传输方向一致，且都是向下传输
                if tc_direction_list[i] == tc_direction_list[i+1] and tc_direction_list[i] == 1:
                    # 有相同的位，此时两门可以进行合并传输
                    for j1 in range(int((len(matrix_list[i]) - 1) / 2)):
                        # 两门具有相同位，且此时的量子位在上方分区
                        if (matrix_list[i][j1] == 1 and 1 == matrix_list[i + 1][j1]) or matrix_list[i][j1] + matrix_list[i + 1][j1] == 3 or (matrix_list[i][j1] == 2 and 2 == matrix_list[i + 1][j1]):
                            # 满足以上所有推荐这两个门可以合并传输
                            tc_num -= 1  # 两门合并传输，计算隐形传态传输时，记载在后一个门
                            print(i)
                            print('t向下合并传输一次')
                          #  i -= 1  # 指向下一个门
                    # 跳出当前循环
                            break
                # 两toffoli门传输方向一致，且都是向上传输
                if tc_direction_list[i] == tc_direction_list[i + 1] and tc_direction_list[i] == 0:
                    for j2 in range(int((len(matrix_list[i]) - 1) / 2), len(matrix_list[i]) - 1):
                        if (matrix_list[i][j2] ==1 and 1 == matrix_list[i + 1][j2]) or matrix_list[i][j2] + matrix_list[i + 1][j2] == 3 or (matrix_list[i][j2] == 2 and 2 == matrix_list[i + 1][j2]) :
                            tc_num -= 1
                            print('t向上合并传输一次')
                          #  i -= 1  # 指向下一个门
                    # 跳出当前循环
                            break
                # # 两toffoli门传输方向不同,不可合并传输
                # if tc_direction_list[i] != tc_direction_list[i+1]:
                #     tc_num += 1

            # # 一个门是toffoli,一个门是cnot
            # if (sum(matrix_list[i]) == 4 and sum(matrix_list[i+1]) == 5) or (sum(matrix_list[i]) == 5 and sum(matrix_list[i+1]) == 4):

            # 两个门都是cnot
            if sum(matrix_list[i]) == 4 and sum(matrix_list[i + 1]) == 4:
                # 两集合有交集，则存在共同元素，可隐形传态
                same_qbit_list = list(set(matrix_list_to_gate_list(matrix_list[i])) & set(matrix_list_to_gate_list(matrix_list[i+1])))
                # 存在两相同量子位，则传输方向任意
                if len(same_qbit_list) == 2:
                    tc_num -= 1
                # 有一相同量子位，且在上半分区
                if len(same_qbit_list) == 1 and same_qbit_list[0] < int(qbit/2) :
                    tc_direction = 1 # 此为i+1的传输方向
                    if tc_direction == tc_direction_list[i] or tc_direction_list[i] == -1:
                        tc_num -= 1
                        print('c合并传输')
                        tc_direction_list[i + 1] = 1
                 # 有一相同量子位，且在下半分区
                if len(same_qbit_list) == 1 and same_qbit_list[0] >= int(qbit / 2):
                    tc_direction = 0  # 此为i+1的传输方向
                    if tc_direction == tc_direction_list[i] or tc_direction_list[i] == -1:
                        tc_num -= 1
                        tc_direction_list[i + 1] = 0
                        print('c合并传输')
            '''一个是toffoli,一个是cnot'''
            if (sum(matrix_list[i]) == 5 and sum(matrix_list[i + 1]) == 4):
                same_qbit_list = list(set(matrix_list_to_gate_list(matrix_list[i])) & set(
                  matrix_list_to_gate_list(matrix_list[i + 1])))
                # toffoli向下传输
                if tc_direction_list[i] == 1:
                    for ci in range(int(len(matrix_list[i]) - 1)):
                        # 找toffoli目标位
                        if matrix_list[i][ci] == 2:
                            t_target = ci
                    # toffoli目标位在交集中，则可以合并传输
                    if t_target in same_qbit_list:
                        tc_direction_list[i + 1] = 1
                        tc_num -= 1
                        print('54tc合并向下传输')
            # toffoli向上传输
                if tc_direction_list[i] == 0:
                    for cj in range(len(matrix_list[i]) - 1):
                       # 找toffoli目标位
                        if matrix_list[i][cj] == 2:
                           t_target = cj
                # toffoli目标位在交集中，则可以合并传输
                    if t_target in same_qbit_list:
                        tc_direction_list[i + 1] = 0
                        tc_num -= 1
                        print('54tc合并向上传输')
            # 一个是toffoli,一个是cnot
            if (sum(matrix_list[i]) == 4 and sum(matrix_list[i + 1]) == 5):
                same_qbit_list = list(set(matrix_list_to_gate_list(matrix_list[i])) & set(
                   matrix_list_to_gate_list(matrix_list[i + 1])))
               # toffoli向下传输
                if tc_direction_list[i + 1] == 1 and tc_direction_list[i] != 0:
                    for ci in range(int(len(matrix_list[i + 1]) - 1)):
                       # 找toffoli目标位
                       if matrix_list[i + 1][ci] == 2:
                           t_target = ci
                    # toffoli目标位在交集中，则可以合并传输
                    if t_target in same_qbit_list:
                        tc_direction_list[i] = 1
                        tc_num -= 1
                        print('45tc合并向下传输')
            # toffoli向上传输
                if tc_direction_list[i + 1] == 0 and tc_direction_list[i] != 1:
                    for cj in range(len(matrix_list[i + 1]) - 1):
                        # 找toffoli目标位
                        if matrix_list[i + 1][cj] == 2:
                            t_target = cj
                # toffoli目标位在交集中，则可以合并传输
                    if t_target in same_qbit_list:
                        tc_direction_list[i] = 0
                        tc_num -= 1
                        print('45tc合并向上传输')

        i += 1
    return matrix_list,tc_num

if __name__ == '__main__':
    matrix_list = [[1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1], [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 1], [0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2, 0, 1], [0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 1], [0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1]]
    print(matrix_list)
    print(len(matrix_list))
   # print(sum(matrix_list[-1]))
    new_matrix_list = delete_useless_gate(matrix_list)
    print(len(new_matrix_list))
    print(new_matrix_list)
    print(judge_tc_direction(matrix_list))
    print(toffoli_distributed(matrix_list,judge_tc_direction(matrix_list),5)[1])

