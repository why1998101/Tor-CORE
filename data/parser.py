#!/usr/bin/env python3

import sys

f = open(sys.argv[1], 'r')
lines = f.readlines()
f.close()

cs = 0
ce = 0
mys = 0
result = []

for line in lines:
	tmp = line.split()
	if (tmp[0]== "S"):
		cs = float(tmp[1])
	else:
		ce = float(tmp[1])
		mys = float(tmp[2])
		rtt = ce-cs
		result.append([rtt, mys/rtt])

cnt = 0
c_time = 0
c_good = 0
for i in result:
	cnt = cnt + 1
	c_time += i[0]
	c_good += i[1]

ff = open("fast_report.txt", 'w+')

s = "Average RTT: "+str(c_time/cnt)+"\n"
ff.write(s)
print(s)

s = "Average Goodput: "+str(c_good/cnt)+"\n"
ff.write(s)
print(s)

for i in result:
	k = str(i[0]) + " "+ str(i[1]) + "\n"
	ff.write(k)


ff.close()
