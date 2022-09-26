OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg c[5];
cx q[2], q[1];
cx q[1], q[2];
cx q[3], q[2];
cx q[2], q[3];
ccx q[4], q[3], q[2];
ccx q[2], q[1], q[0];
ccx q[4], q[3], q[2];
ccx q[2], q[1], q[0];
cx q[1], q[0];
ccx q[3], q[4], q[2];
ccx q[2], q[1], q[0];
ccx q[4], q[3], q[2];
ccx q[2], q[1], q[0];
cx q[1], q[0];
cx q[4], q[3];
cx q[3], q[4];
ccx q[3], q[2], q[1];
ccx q[2], q[1], q[0];
ccx q[3], q[2], q[1];
ccx q[1], q[2], q[0];
cx q[0], q[4];

// @columns [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]