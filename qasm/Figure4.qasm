# 
# File:   test1.qasm
# Date:   22-Mar-04
# Author: I. Chuang <ichuang@mit.edu>
#
# Sample qasm input file - EPR creation
#
        qubit 	q0 #A little info
        qubit 	q1
		qubit 	q2
		qubit 	q3

	cnot	q0,q1
	cnot	q2,q0
	cnot	q0,q3
	h	q3
	cnot	q3,q1
	h	q1
	cnot	q1,q3
	cnot	q0,q1
	cnot	q3,q0
