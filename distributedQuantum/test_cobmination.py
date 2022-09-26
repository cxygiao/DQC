import copy
from audioop import avg
import pandas as pd
import re
import math
import itertools
import random
import numpy

Population_size = 10  # 种群大小

def line_sequence_change_combination(qbit):
    str1 = ''
    final_line_sequence_combination = []
    # 最多支持 26量子位
    str2 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A',
            'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
    for i in range(int(qbit)):
        # str1：ABCDEFGHIJKL.... 共qbit个
        str1 = str1 + str2[i]
    print(str1)
    # 排列组合 将str1按qibt/2 一分为，共有C(qbit/2,qbit)种情况
    line_sequence_combination = []  # 线序排列集合['ABCDEF', 'ABCDEG', 'ABCDEH', 'ABCDEI', 'ABCDEJ', 'ABCDEK', 'ABCDEL', 'ABCDFG', 'ABCDFH', 'ABCDFI', 'ABCDFJ'......]
    count = 0
    interval = int(Combinatorial(qbit, int(qbit / 2))) / Population_size
    print(interval)
    for p in itertools.combinations(str1, int(int(qbit) / 2)):
        #  print(''.join(i), end=" ")
        # print(''.join(i))
        for k in range(0,int(Combinatorial(qbit, int(qbit / 2))) ,int(interval)):
            # print('1111',end=' ')
            # print(count,end=' ')
            # print(k)
            if count == k:
               line_sequence_combination.append(''.join(p))
        count = count + 1
    print(count)
    #     print(line_sequence_combination)
    # j = 0
    # while j < Population_size:
    #     line_sequence_combination.append()

    for j in range(len(line_sequence_combination)):
        print(single_to_all_line_sequence(line_sequence_combination[j], qbit))
        final_line_sequence_combination.append(single_to_all_line_sequence(line_sequence_combination[j], qbit))
    return final_line_sequence_combination

'''根据前半部分线序推出全部线序  ABCDFG =>ABCDFGEHIJKL'''
def single_to_all_line_sequence(line_sequence_combination,qbit):
    # str2 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    str2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9','!','@']
    all_line_sequence = list(line_sequence_combination)

    for i in range(int(qbit)):
        if str2[i] not in all_line_sequence:
            all_line_sequence.append(str2[i])
    new_all_line_sequence = "".join(all_line_sequence)
    return new_all_line_sequence

# 生成初始线序 返回10个随机的初始线序
def generate_initial_line_sequence(qbit):
    initial_line_sequence = []
    str1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9','!','@']
    print(len(str1))
    # 首位线序 abcdefg...
    single_line_sequence = str1[:qbit]
    print(''.join(single_line_sequence))
    # 生成十个随机的初始线序
    for i in range(Population_size):
        random.shuffle(single_line_sequence)
        initial_line_sequence.append(''.join(single_line_sequence))
    return initial_line_sequence


def Combinatorial(n,i):
    '''设计组合数'''
    #n>=i
    Min=min(i,n-i)
    result=1
    for j in range(0,Min):
        #由于浮点数精度问题不能用//
        result=result*(n-j)/(Min-j)
    return  result

if __name__ == '__main__':
    # com = line_sequence_change_combination(32)
    # print(com)
    # print(len(com))
    print(generate_initial_line_sequence(64))
    print(int(Combinatorial(6, 3)))