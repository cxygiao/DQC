OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];
creg c[12];

ccx q[6],q[7],q[10];
ccx q[8],q[10],q[11];
ccx q[7],q[8],q[10];
cx q[5],q[7];
cx q[7],q[5];
cx q[5],q[7];
cx q[0],q[6];
ccx q[9],q[11],q[7];
cx q[6],q[0];
ccx q[9],q[10],q[11];
cx q[0],q[6];
ccx q[8],q[9],q[10];
ccx q[11],q[6],q[7];
ccx q[6],q[10],q[11];
ccx q[6],q[9],q[10];
cx q[1],q[8];
cx q[8],q[1];
cx q[1],q[8];
ccx q[11],q[8],q[7];
ccx q[8],q[10],q[11];
ccx q[6],q[8],q[10];
cx q[2],q[9];
cx q[9],q[2];
cx q[2],q[9];
ccx q[11],q[9],q[7];
ccx q[9],q[10],q[11];
ccx q[8],q[9],q[10];
ccx q[11],q[3],q[7];
ccx q[3],q[10],q[11];
ccx q[3],q[9],q[10];
ccx q[11],q[4],q[7];
ccx q[4],q[10],q[11];
cx q[11],q[4];
cx q[1],q[8];
cx q[8],q[1];
cx q[1],q[8];
cx q[1],q[8];
cx q[8],q[1];
cx q[1],q[8];