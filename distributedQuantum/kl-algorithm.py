# coding = utf-8

#list存储方式 kl算法 电路划分
# 2021.10.20
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

# 用邻接表处理图
def graph(listGate):
    # 顶点
    vertex = 4
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

# KL算法求解最小全局门数量
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



if __name__ == '__main__':
    pd.set_option('display.max_columns', 28)  # 给最大列设置为10列
    pd.set_option('display.max_rows', 100)  # 设置最大可见100行
    input_filename = 'D:/qasm/6169940b83e9060a6a5194b0.qasm'
    listGate = converter_circ_from_qasm(input_filename)

    print(listGate)

    adjacencyList = graph(listGate)
    print(adjacencyList)
    kllist = []
    minGateNumList =[]
    bestklList = []
    minGateNum = len(adjacencyList)
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
        print('全局门数量'+str(minMun))
        # minGateNumList=[545545]   求最小全局门数
        if minGateNumList[i] < minGateNum:
           minGateNum = minGateNumList[i]

        kllist = copy.deepcopy(kl(nnewlist)[1])
        print('mainkllist',end='')
        print(kllist)
        if kllist[-1] == minGateNum:
           bestklList=copy.deepcopy(kllist)
        print('')
   # print(minGateNumList)

 #   for i in range (len(minGateNumList)):

    print('最小全局门数量：'+str(minGateNum))
    print('最优解：',end='')
    print(bestklList)













