#!/usr/bin/env python
"""
    SimulatorTest.py
    Run Simulation Given Snapshots
    zhihua.lai@ranplan.co.uk
"""

from sys import *
from time import *
from socket import *
from subprocess import Popen, PIPE, STDOUT

def usage():
    print "%s System Snapshots" % argv[0]

def gettime():
    return strftime("%I:%M:%S %p", localtime(time()))

def launch(system, snapshots):
    """
        Launch the simulations ...
    """    
    ms = snapshots
    print(gettime() + ": " + gethostname() + " " + system + " " + "running " + str(snapshots) + " snapshots...")
    cmd = ["HetNetSimulator.exe", "--SYSTEM", system, "--TTI", str(snapshots)]
    print ' '.join(cmd);
    sleep(int(ms * 0.05))
    #p = Popen(' '.join(cmd), shell=True, stdout=PIPE, stderr=STDOUT)
    #for line in p.stdout.readlines():
    #    print line
    #retval = p.wait()
    print(gettime() + ": " + gethostname() + " finishes " + system + " " + str(snapshots) + " snapshots.")
    
if __name__ == "__main__":
    if len(argv) != 3:
        usage()
    elif argv[2].isdigit():
        launch(argv[1], int(argv[2]))
    else:
        usage()
        
