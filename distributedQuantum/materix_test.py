import copy

import pandas as  pd
import re
import math
import itertools

def merge_transmission_with_recursion(matrix_list):
    # for i in range(len(matrix_list)-1):
    i = 0
    ii = 0
    # # 删除无用局部门 即在对方分区的局部门
    # while ii < len(matrix_list):
    #     is_local_gate = 0  # 是否为对方分区局部门
    #     for iii in range(0, int((len(matrix_list[0]) - 1) / 2) ):
    #         is_local_gate = is_local_gate + matrix_list[ii][iii]
    #     if is_local_gate == 0: #当前分区量子位上所有值的和为0，则在此分区无门
    #         del matrix_list[ii]
    #         ii -= 1
    #     ii += 1

    matrix_size = len(matrix_list[0])-1
    while i < len(matrix_list)-1:
        # 此处要考虑：是否相邻两个门都是全局门才可以合并矩阵，还是不管是否都是全局门，也可以合并
        if len(matrix_list[i]) != 0 :
            # 两门都是全局门，才可以合并传输
       # if matrix_list[i][-1] == 1 and matrix_list[i + 1][-1] == 1:
            for j in range(4):
                # 两门具有相同控制位  [1,0,0,2][1,0,2,0] =>[1,0,2,2]
                if matrix_list[i][j] == 1 and matrix_list[i+1][j] ==1:
                    matrix_list[i][j] -= 1  # 在合并矩阵时，相同的控制位不变
                    for k in range(matrix_size):  # 在合并矩阵时，除控制位以外的其他量子位，相加
                        matrix_list[i][k] += matrix_list[i+1][k]  # 至此，相同控制位情况下，矩阵合并相加完成！
                    del matrix_list[i+1]    # 合并完成后需要删除后一个矩阵
                    i -= 1
                    break
                # 一门合并完成时，无法和下一个门合并，跳出当前循环
                if matrix_list[i][j] == 3 and matrix_list[i+1][j] == 0:
                    break
                # 一门控制位是另外一门的目标位 [1,0,0,2][2,0,1,0] =>[3,0,1,2]
                if (matrix_list[i][j] == 1 and matrix_list[i+1][j] ==2) or (matrix_list[i][j] == 2 and matrix_list[i+1][j] ==1):
                    for kk in range(matrix_size):  # 在合并矩阵时，所以量子位，相加
                        matrix_list[i][kk] += matrix_list[i+1][kk]  # 至此，一门控制位是另外一门的目标位情况下，矩阵合并相加完成！
                    del matrix_list[i + 1]  # 合并完成后需要删除后一个矩阵
                    i -= 1
                    break
                # 考虑多重合并
                if matrix_list[i][j] >= 3 and matrix_list[i][j]==1:
                    for kkk in range(matrix_size):  # 在合并矩阵时，所以量子位，相加
                        matrix_list[i][kkk] += matrix_list[i+1][kkk]
                    del matrix_list[i + 1]  # 合并完成后需要删除后一个矩阵
                    i -= 1
                    break
        i += 1
    transmissions_number_by_matrix = 0 # 隐形传态次数
    for t in range(len(matrix_list)):
        transmissions_number_by_matrix += matrix_list[t][-1]
    return matrix_list,transmissions_number_by_matrix

''' 倒序判断能否合并传输'''
'''无法解决合并传输时，间隔门的合并传输
思路1:矩阵中的状态码新增-1，0，1；代表上半分区和下半分区，以及全局门
思路2：或者考虑直接在遍历中判断在哪个分区
思路3：在矩阵list中直接删除在非此分区的门'''
def merge_transmission_with_recursion_by_reverse_order(matrix_list):
    # for i in range(len(matrix_list)-1):
    i = 0

    # 直接删除在上半分区的局部门
    # is_global_gate = 1 # 判断是否为全局门
    # local_gate = 1 # 判断是否为局部门
    # for ii in range(len(matrix_list)):
    #    for iii in range(int(matrix_size/2)):
    #        # 量子位上不为0，即在此量子位上存在控制位或目标位。
    #        # 目标位和控制位都存在于上半分区，则可删除此门
    #        if matrix_list[ii][iii] != 0:
    #            local_gate = 0 # 不是局部梦
    #        else:
    #            local_gate = 1
    #    is_global_gate = is_global_gate & local_gate
    #    print(is_global_gate)
    #    if is_global_gate == 0:
    #        del matrix_list[ii]

    # 换一种思路，从下往上判断是否为上班分区局部门
    ii = 0
   # for ii in range(len(matrix_list)):
    while ii < len(matrix_list):
        is_local_gate = 0
        for iii in range(len(matrix_list[0])-2,int((len(matrix_list[0]) - 1)/2)-1,-1):
            is_local_gate = is_local_gate + matrix_list[ii][iii]
            # if matrix_list[ii][iii] == 0:
            #     is_local_gate = 1
            # else:
            #     is_local_gate = 0
        if is_local_gate == 0:
            del matrix_list[ii]
            ii -= 1
        ii +=1
   # print(matrix_list)
    matrix_size = len(matrix_list[0]) - 1
    while i < len(matrix_list)-1:
        # 两门都是全局门，才可以合并传输
        if len(matrix_list[i]) != 0:
       # if matrix_list[i][-1] == 1 and matrix_list[i + 1][-1] == 1:
            for j in range(matrix_size-1,0,-1):
                # 两门具有相同控制位  [1,0,0,2][1,0,2,0] =>[1,0,2,2]
                if matrix_list[i][j] == 1 and matrix_list[i+1][j] ==1:
                    matrix_list[i][j] -= 1  # 在合并矩阵时，相同的控制位不变
                    for k in range(matrix_size-1,0,-1):  # 在合并矩阵时，除控制位以外的其他量子位，相加
                        matrix_list[i][k] += matrix_list[i+1][k]  # 至此，相同控制位情况下，矩阵合并相加完成！
                    del matrix_list[i+1]    # 合并完成后需要删除后一个矩阵
                    i -= 1
                    break
                # 一门合并完成时，无法和下一个门合并，跳出当前循环
                if matrix_list[i][j] == 3 and matrix_list[i+1][j] == 0:
                    break
                # 一门控制位是另外一门的目标位 [1,0,0,2][2,0,1,0] =>[3,0,1,2]
                if (matrix_list[i][j] == 1 and matrix_list[i+1][j] ==2) or (matrix_list[i][j] == 2 and matrix_list[i+1][j] ==1):
                    for kk in range(matrix_size-1,0,-1):  # 在合并矩阵时，所以量子位，相加
                        matrix_list[i][kk] += matrix_list[i+1][kk]  # 至此，一门控制位是另外一门的目标位情况下，矩阵合并相加完成！
                    del matrix_list[i + 1]  # 合并完成后需要删除后一个矩阵
                    i -= 1
                    break
                # 考虑多重合并
                if (matrix_list[i][j] >= 3 and matrix_list[i+1][j]==1) :
                    for kkk in range(matrix_size-1,0,-1):  # 在合并矩阵时，所以量子位，相加
                        matrix_list[i][kkk] += matrix_list[i+1][kkk]
                    del matrix_list[i + 1]  # 合并完成后需要删除后一个矩阵
                    i -= 1
                    break
        i += 1
    transmissions_number_by_matrix = 0 # 隐形传态次数
    for t in range(len(matrix_list)):
        transmissions_number_by_matrix += matrix_list[t][-1]
    return matrix_list,transmissions_number_by_matrix


if __name__ == '__main__':
    #matrix_list = [[1, 2, 0, 0, 0], [2, 0, 1, 0, 1], [1, 0, 0, 2, 1], [0, 2, 0, 1, 1], [0, 1, 0, 2, 1], [1, 2, 0, 0, 0], [2, 0, 0, 1, 1]]
    #matrix_list = [[1,2,0,0,0,0,0],[1,0,0,0,0,2,1],[1,0,2,0,0,0,0],[2,0,1,0,0,0,0],[0,0,2,0,1,0,1],[0,0,0,0,1,2,0],[0,0,2,0,1,0,1],[1,0,0,0,0,2,1]]
    matrix_list = [[1,1,0,0,0,0],[0,2,1,0,0,0],[0,1,2,0,0,0],[0,0,2,1,0,1],[0,0,1,2,0,1],[0,0,0,2,1,0],[0,0,0,1,2,0],[0,0,0,2,1,0],[0,0,2,0,1,1],[0,2,0,0,1,1],[2,0,0,0,1,1]]
    print('初始矩阵：', end='')
    print(matrix_list)
    matrix_list_by_reverse_order = copy.deepcopy(matrix_list) # 反序矩阵
    multi_transmission_list = merge_transmission_with_recursion(matrix_list)[0]
    print(multi_transmission_list)
    print('通过矩阵合并求出的隐形传态次数（默认位全部向下传输）:' + str(merge_transmission_with_recursion(matrix_list)[1] * 2))

    multi_transmission_list_order = merge_transmission_with_recursion_by_reverse_order(matrix_list_by_reverse_order)[0]
    print(multi_transmission_list_order)
    print('通过矩阵合并求出的隐形传态次数（默认位全部向上传输）:' + str(merge_transmission_with_recursion_by_reverse_order(matrix_list_by_reverse_order)[1] * 2))