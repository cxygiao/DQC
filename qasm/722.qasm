OPENQASM 2.0;
include "qelib1.inc";

qreg q[6];
creg c[6];

cx q[1], q[4];
cx q[0], q[3];
cx q[0], q[5];
cx q[4], q[0];
cx q[3], q[1];
cx q[2], q[5];
cx q[4], q[1];
cx q[0], q[2];

// @columns [0,1,2,3,4,5,6,7]