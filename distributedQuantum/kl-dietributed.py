# coding = utf-8

# 1.kl算法进行电路划分
# 2.矩阵实现减少隐形传态（合并传输）
# 1、2不能分开考虑，每划分一次，就要计算一次最小的隐形传态次数，然后将划分结果和最小隐形传态次数存入list。
# 只考虑相邻两个门的同时隐形传态，未考虑有间隔情况能否同时隐形传态
# 未考虑电路移动！后续考虑电路移动还能继续减少隐形传态次数

# 2021.10.25 code in 12-402
# 陈新宇

"""
字符串表达式 获取门的位置
"""
import copy

import pandas as  pd
import re
import math
import itertools

minGateList =[]


def get_data(str):
    pattern = re.compile("[\d]+")
    result = re.findall(pattern, str)
    return result

'''
读取整个qasm文件
'''
def converter_circ_from_qasm(input_file_name):
 #   df_ori_qc = pd.DataFrame(columns=['k', 'c', 't'])  # 近邻化 以dataframe形式存储的近邻化量子电路
    listGate =[]

    qasm_file = open(input_file_name, 'r')
    iter_f = iter(qasm_file)
    reserve_line = 4
    num_line = 0
    for line in iter_f:  # 遍历文件，一行行遍历，读取文本
        num_line += 1
        if num_line <= reserve_line:
            continue
        else:
            if line[0:2] == 'CX' or line[0:2] == 'cx':
                '''获取CNOT'''
                cnot = get_data(line)
                cnot_control = cnot[0]
                cnot_target = cnot[1]
                listSingle=[cnot_control,cnot_target]
                listGate.append(listSingle)

    return listGate

'''
用邻接表处理图
'''
def graph(listGate):
    # 顶点
    vertex = 5
    # 边数
    edge = 4
    # 邻接表
    adjacencyList = []
    str1 = ''
    #将int4化为str01234,便于下步排列组合01 02 03 12 13 23
    for i in range(vertex):
        str1 = str1+str(i)
    # 通过listGate转换为邻接表，即化简listGate,添加权值
    for i in itertools.combinations(str1, 2):
        a = ''.join(i)
        j=0
        for i in range(len(listGate)):
            if (listGate[i][0]==a[0] and listGate[i][1]==a[1]) or (listGate[i][0]==a[1] and listGate[i][1]==a[0]):
               j+=1
        sonlist = [a[0], a[1],j]

        adjacencyList.append(sonlist)

    return adjacencyList

'''
KL算法求解最小全局门数量
'''
def kl(adjacencyList):
    minMun = 0
    weight = 0
    minweight = 0
    weightAndKlistList =[]
    kllist = copy.deepcopy(adjacencyList)
    # 计算权值总和，即所有门的数目
    for i in range(len(adjacencyList)):
        weight = weight + adjacencyList[i][2]
   # print('weight'+str(weight))

    # 只计算12 34分区/只计算一趟
    # 将首个门与后面的门进行配对，不能配对的将权值变为-1
   # for i in range(len(adjacencyList)):
    for j in range(1,len(adjacencyList)):
        if(adjacencyList[0][0] is kllist[j][0] or adjacencyList[0][0] is kllist[j][1] or adjacencyList[0][1] is kllist[j][0] or adjacencyList[0][1] is kllist[j][1]):
            kllist[j][2]=-1
    # 计算最小权值，即全局门的最小数  权值为-1即为全局门
    for i in range(len(adjacencyList)):
        if(kllist[i][2]!=-1):
            minMun=minMun+kllist[i][2]
    minweight=weight-minMun
    kllist.append(minweight)

    print('kllist',end='')
    print(kllist)
    print('adjacencyList',end='')
    print(adjacencyList)

    return minweight,kllist

'''两门合并传输时可以减少隐形传态次数，计算此时的隐形传态次数'''
def double_merge_transmissions(listD,listGate):
    j = 0
    count = 0
    while (j < len(listD) - 1):
        if (listD[j][2] == listD[j + 1][2] == 1) and (len(list(set(listGate[j]) & (set(listGate[j + 1])))) >= 1):
            count += 1
        #    print('--执行一次')
            print(str(listD[j]) + ' ' + str(listD[j + 1])+'一起传输')
            j += 2
        else:
            j += 1
   # print(count)
    double_merge_transmissions_number = (minMun - count) * 2
    return double_merge_transmissions_number

'''考虑多门合并传输时，减少隐形传态次数。
   返回：最小隐形传态次数
'''
'''思路：
1.从左往右扫描，查找有相同量子位全局门，把这些全局门放入一个list。
2.判断这个list中的全局门受否收到局部门的影响，导致无法一起传输。如果收到影响，就从list中倒序删除受影响的门。
  2.1 某一个list:[[1,2,5,-1],[3,4,0]，[7,-1]] ，-1，0代表在哪个分区执行，即往哪个分区隐形传态。
  2.2 list 要考虑向哪个方向传输！！！
3.根据各个list求出隐形传态次数
'''
# def multi_merge_transmission(listD,listGate):
#     for i in range(len(listD)-1):
#         if (listD[i][-1]==1 and listD[i][-1]==1) and (len(list(set(listGate[j]) & (set(listGate[j + 1])))) >= 1) : #两门都是全局门，且有相同的量子位
#
#     multi_merge_transmission_number = 0
#     return multi_merge_transmission_number

'''用递归方法处理多门合并传输'''
'''matrix_list:[[1, 2, 0, 0, 0], [2, 0, 1, 0, 1], [1, 0, 0, 2, 1], [0, 2, 0, 1, 1], [0, 1, 0, 2, 1], [1, 2, 0, 0, 0], [2, 0, 0, 1, 1]]'''
def merge_transmission_with_recursion(matrix_list):
    # for i in range(len(matrix_list)-1):
    i = 0
    matrix_size = len(matrix_list[0]) - 1
    while i < len(matrix_list)-1:
        # 两门都是全局门，才可以合并传输
        if matrix_list[i][-1] == 1 and matrix_list[i + 1][-1] == 1:
            for j in range(matrix_size):
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
                #  # 两门互不影响,则交换两门位置 [1,0,0,2][0,1,2,0] =>[0,1,2,0][1,0,0,2]
                # if (matrix_list[i][j] == 1 and matrix_list[i+1][j] ==0) or (matrix_list[i][j] == 2 and matrix_list[i+1][j] ==0):
                #     temporary_matrix_list = matrix_list[i]  # 临时矩阵，用于交换
                #     matrix_list[i] = copy.deepcopy(matrix_list[i+1])
                #     matrix_list[i+1] = temporary_matrix_list
                #     break
                # else: # 无法合并或者交换
                #     continue
        i += 1
    transmissions_number_by_matrix = 0 # 隐形传态次数
    for t in range(len(matrix_list)):
        transmissions_number_by_matrix += matrix_list[t][-1]
    return matrix_list,transmissions_number_by_matrix

''' 倒序判断能否合并传输'''
def merge_transmission_with_recursion_by_reverse_order(matrix_list):
    # for i in range(len(matrix_list)-1):
    i = 0
    matrix_size = len(matrix_list[0]) - 1
    while i < len(matrix_list)-1:
        # 两门都是全局门，才可以合并传输
        if matrix_list[i][-1] == 1 and matrix_list[i + 1][-1] == 1:
            for j in range(matrix_size,0,-1):
                # 两门具有相同控制位  [1,0,0,2][1,0,2,0] =>[1,0,2,2]
                if matrix_list[i][j] == 1 and matrix_list[i+1][j] ==1:
                    matrix_list[i][j] -= 1  # 在合并矩阵时，相同的控制位不变
                    for k in range(matrix_size,0,-1):  # 在合并矩阵时，除控制位以外的其他量子位，相加
                        matrix_list[i][k] += matrix_list[i+1][k]  # 至此，相同控制位情况下，矩阵合并相加完成！
                    del matrix_list[i+1]    # 合并完成后需要删除后一个矩阵
                    i -= 1
                    break
                # 一门合并完成时，无法和下一个门合并，跳出当前循环
                if matrix_list[i][j] == 3 and matrix_list[i+1][j] == 0:
                    break
                # 一门控制位是另外一门的目标位 [1,0,0,2][2,0,1,0] =>[3,0,1,2]
                if (matrix_list[i][j] == 1 and matrix_list[i+1][j] ==2) or (matrix_list[i][j] == 2 and matrix_list[i+1][j] ==1):
                    for kk in range(matrix_size,0,-1):  # 在合并矩阵时，所以量子位，相加
                        matrix_list[i][kk] += matrix_list[i+1][kk]  # 至此，一门控制位是另外一门的目标位情况下，矩阵合并相加完成！
                    del matrix_list[i + 1]  # 合并完成后需要删除后一个矩阵
                    i -= 1
                    break
                # 考虑多重合并
                if matrix_list[i][j] >= 3 and matrix_list[i][j]==1:
                    for kkk in range(matrix_size,0,-1):  # 在合并矩阵时，所以量子位，相加
                        matrix_list[i][kkk] += matrix_list[i+1][kkk]
                    del matrix_list[i + 1]  # 合并完成后需要删除后一个矩阵
                    i -= 1
                    break
        i += 1
    transmissions_number_by_matrix = 0 # 隐形传态次数
    for t in range(len(matrix_list)):
        transmissions_number_by_matrix += matrix_list[t][-1]
    return matrix_list,transmissions_number_by_matrix


'''主函数'''
if __name__ == '__main__':
    pd.set_option('display.max_columns', 28)  # 给最大列设置为10列
    pd.set_option('display.max_rows', 100)  # 设置最大可见100行
    input_filename = 'D:/qasm/6169940b83e9060a6a5194b0.qasm'
   # input_filename = 'qasm/Fi'
    listGate = converter_circ_from_qasm(input_filename)

    print('listgate'+str(listGate))

    adjacencyList = graph(listGate)
    print('adjacencylist'+str(adjacencyList))
    kllist = []
    minGateNumList =[]

    # 最优解
    bestklList = []
    # 最小全局门数量
    minGateNum = len(adjacencyList)

    #最小隐形传态次数
    minTeleportation = len(adjacencyList)*2

    # 依次将每个门移到list的第一位
    for i in range(len(adjacencyList)):
        newkllist = [['0', '0', 0]]
        nnewlist = []
        nnewlist = nnewlist + newkllist
        nnewlist[0]=adjacencyList[i]
      #  print(nnewlist)

        nnewlist=nnewlist+adjacencyList
        del nnewlist[i+1]
        # 计算全局门的数量
        minMun = kl(nnewlist)[0]

        minGateNumList.append(minMun)
        print('全局门数量：'+str(minMun))
        print('未化简前最小隐形传态次数：'+str(minMun*2))
        # minGateNumList=[545545]   求最小全局门数
        if minGateNumList[i] < minGateNum:
           minGateNum = minGateNumList[i]

        kllist = copy.deepcopy(kl(nnewlist)[1])
        kllist.pop(-1)
        print('mainkllist',end='')
        print(kllist)

        # listD：在电路划分后，门是否为全局门 【0，1，1】末尾0表示局部门，1表示全局门

        listD = copy.deepcopy(listGate)
        print('listD:'+str(listD))

        #分离出子系统的有效量子位
        effectiveList = copy.deepcopy(kllist)
        for j in range(len(effectiveList)-1,-1,-1):
            if effectiveList[j][2]==-1:
                effectiveList.pop(j)
        # 删除list中状态码
        for p in range(len(effectiveList)):
            del effectiveList[p][2]
        #  print('efflist'+str(effectiveList))
        # 将efflist反序复制，[['2', '3'], ['0', '1']]  =》 [['2', '3'], ['0', '1'], ['3', '2'], ['1', '0']]
        for p in range(len(effectiveList)):
            efflist = []
            efflista = effectiveList[p][0]
            efflistb = effectiveList[p][1]
            efflist.append(efflistb)
            efflist.append(efflista)
            effectiveList.append(efflist)
        print('efflist' + str(effectiveList))

        # 将listD中局部门状态码置0
        for k in range(len(listD)):
           # listD[k].append(0)
            if listD[k] in effectiveList:
                #局部门
                listD[k].append(0)
            else:
                #全局门
                listD[k].append(1)
        print('带状态码的listD'+str(listD))

        matrix_list = []  #矩阵list [[1,0,0,2,1] ,[1,2,0,,0]]
        for s in range(len(listD)):
            matrix_son_list = [0,0,0,0,0]
            matrix_son_list[int(listD[s][0])] = 1
            matrix_son_list[int(listD[s][1])] = 2
            matrix_son_list[-1] = listD[s][-1]
            matrix_list.append(matrix_son_list)
        print('门的矩阵形式：'+str(matrix_list))

# 10.27晚 写到这 考虑是否用矩阵代替list存储电路 考虑将多个门合并传输
   # print(minGateNumList)
 #   for i in range (len(minGateNumList)):
    # print('最小全局门数量：'+str(minGateNum))
    # print('最优解：',end='')
    # print(bestklList)

        #####################################
        # 下面进行减少隐形传态 即通过合并传输减少传输
     #  for j in range (len(listD)-1):
         #   print(str(listD[j][2])+' '+ str(listD[j+1][2]))
         #   print(len(list(set(listGate[j])&(set(listGate[j+1])))))

         # 通过状态码判断相邻两个门能否合并传输
         # 求并集 判断是否有同一量子位上的
        # j=0
        # count=0
        # while(j<len(listD)-1):
        #     if(listD[j][2] == listD[j+1][2] ==1) and (len(list(set(listGate[j])&(set(listGate[j+1]))))>=1 ):
        #         count+=1
        #         print('--执行一次')
        #         print(str(listD[j]) + ' ' + str(listD[j + 1]))
        #         j+=2
        #     else:
        #         j +=1
        # print(count)
        # print("只考虑相邻两门合并传输的次数："+str((minMun-count)*2))

        #注意此处变量名不能和函数名重复，不然会报错
        transmissions_number = double_merge_transmissions(listD,listGate)
        print("只考虑相邻两门合并传输的次数：" + str(transmissions_number))
        # 矩阵合并
        matrix_list_by_reverse_order = copy.deepcopy(matrix_list)  # 反序矩阵
        multi_transmission_list = merge_transmission_with_recursion(matrix_list)[0]
        print(multi_transmission_list)
        print('通过矩阵合并求出的隐形传态次数（默认位全部向下传输）:'+str(merge_transmission_with_recursion(matrix_list)[1]*2))
        multi_transmission_list_order = merge_transmission_with_recursion_by_reverse_order(matrix_list_by_reverse_order)[0]
        print(multi_transmission_list_order)
        print('通过矩阵合并求出的隐形传态次数（默认位全部向上传输）:' + str(
            merge_transmission_with_recursion_by_reverse_order(matrix_list_by_reverse_order)[1] * 2))
        print('')
