import copy
import numpy
import random
import qiskit.circuit.library.basis_change.qft as qft

from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
from qiskit import QuantumCircuit
from qiskit import Aer, transpile
from qiskit.tools.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi

lista =[2,1]
listb = [1,2]
union = list(set(lista).union(set(listb)))
ret= list(set(lista) & set(listb))
print(union)
print(ret)

listc = ['2', '9', '10', 1]
print(len(listc))

str1 = 'G'
print(ord(str1)-65)

str2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
all_line_sequence = list('ABEFGD')
print(all_line_sequence)
for i in range(12):
    if str2[i] not in all_line_sequence:
        all_line_sequence.append(str2[i])
print(all_line_sequence)


str3 = 'asdfg'
print(str3[4])
print(str3)

matrix_list = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1],
     [0, 1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 1],
     [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 0, 1], [0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1],
     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 2, 0, 1],
     [0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 2, 1],
     [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2, 0, 1], [0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 0, 0, 1],
     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 2, 0, 0],
     [0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 2, 0],
     [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0]]
print(sum(matrix_list[11][0:int((len(matrix_list[11])-1)/2)]))
print(sum(matrix_list[11][int((len(matrix_list[11])-1)/2):int(len(matrix_list[11])-1)]))
matrix_list.reverse()
print(matrix_list)

if 2 in [2,3]:
    print(12343223232)

print(max(matrix_list[0]))


lista.extend(listb)
print(lista)

print(numpy.random.rand())

listaaa = [[1],[2]]
listaab = [[2],[2]]
listaaa.extend(listaab)
print(listaaa)

straa = 'asdfghjk'
print(int(len(straa)/2)+1)

print(random.randint(0,3))

straa_list = list(straa)
straa_list[0] = 'p'
print(straa_list)
straa = ''.join(straa_list)
print(straa)

gate_list = [[13, 10], [8, 13], [13, 10], [8, 13], [8, 10], [10, 13], [12, 10], [9, 12], [12, 10], [9, 12], [9, 10], [10, 12], [9, 10], [10, 12], [9, 10], [9, 12], [6, 10], [7, 6], [6, 10], [7, 6], [7, 10], [10, 6], [12, 13], [9, 12], [12, 13], [9, 12], [9, 13], [11, 13], [9, 11], [11, 13], [9, 11], [9, 13], [12, 13], [6, 12], [7, 6], [6, 12], [7, 6], [7, 12], [5, 12], [7, 5], [5, 12], [7, 5], [7, 12], [6, 12], [7, 12], [3, 6], [3, 6], [1, 3], [3, 6], [1, 3], [1, 6], [1, 6], [5, 11], [7, 5], [5, 11], [7, 5], [7, 11], [10, 11], [7, 10], [10, 11], [7, 10], [7, 11], [5, 11], [4, 5], [1, 4], [4, 5], [1, 4], [1, 5], [4, 10], [1, 4], [4, 10], [1, 4], [1, 10], [3, 10], [1, 3], [3, 10], [1, 3], [1, 10], [4, 10], [2, 4], [0, 2], [2, 4], [0, 2], [0, 4], [2, 3], [2, 3], [0, 2], [2, 3], [0, 2], [0, 3], [0, 3]]
gate_list.reverse()
print(gate_list)

def recursive(i):
    sum = 0
    if i == 0:
        return 1
    else:
        sum = i * recursive(i-1)
    return sum

def sum(n):
    v = 1
    for i in range(n):
        v = v + i
    return v


# 返回 x 在 arr 中的索引，如果不存在返回 -1
def binarySearch(arr, l, r, x):
    if r >= l:
        mid = int(l + (r - l) / 2)
        # 元素整好的中间位置
        if arr[mid] == x:
            return mid
            # 元素小于中间位置的元素，只需要再比较左边的元素
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
            # 元素大于中间位置的元素，只需要再比较右边的元素
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        # 不存在
        return 0


Aer.backends()
circ = QuantumCircuit(5)
circuit = qft.QFT(5)
circ.measure_all()

# Transpile for simulator
simulator = Aer.get_backend('aer_simulator')
circ = transpile(circ, simulator)

# Run and get counts
result = simulator.run(circ).result()
counts = result.get_counts(circ)
plot_histogram(counts, title='Bell-State counts')
