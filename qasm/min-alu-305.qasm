OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];
creg c[10];

ccx q[1],q[2],q[4];
ccx q[3],q[4],q[5];
ccx q[1],q[2],q[6];
cx q[2],q[6];
x q[6];
ccx q[0],q[6],q[5];
ccx q[0],q[5],q[6];
cx q[1],q[7];
cx q[2],q[7];
cx q[3],q[8];
cx q[4],q[8];
ccx q[3],q[7],q[8];
ccx q[3],q[4],q[8];
cx q[3],q[9];
ccx q[3],q[4],q[9];
cx q[4],q[9];
x q[9];
ccx q[0],q[9],q[8];
ccx q[0],q[8],q[9];
x q[9];