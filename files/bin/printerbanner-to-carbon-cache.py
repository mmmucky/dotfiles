#!/usr/bin/python


import subprocess
import time

start = int(time.time()) - 30300 # highly tuned, for calling lurbs a douche
timestamp = start

for line in subprocess.check_output(["printerbanner", "lurbs is a douche"]).split('\n'):
    points = []
    state = ' '
    for i in range(0,len(line)):
        if line[i] != state or i==(len(line)-1):
            points.append(i)
            state = line[i]
    metric = 0
    for point in points:
        print 'collectd.lurbs.{} {} {}'.format(metric, point, timestamp)
        metric += 1
    timestamp += 60
