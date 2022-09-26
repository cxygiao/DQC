OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

cx q[4], q[1];
cx q[3], q[0];
cx q[1], q[4];
ccx q[2], q[4], q[3];
ccx q[2], q[3], q[4];
ccx q[1], q[2], q[3];
ccx q[2], q[3], q[4];
ccx q[1], q[2], q[3];

// @columns [0,1,2,3,4,5,6,7]