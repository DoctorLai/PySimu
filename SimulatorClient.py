#!/usr/bin/env python
"""
    SimulatorClient.py
    Client Socket
    zhihua.lai@ranplan.co.uk
"""

import socket, time, threading, sys

class SimulatorClient(threading.Thread):
    """
        Simulator Socket Client
    """

    """
        private attributes
    """
    __port = 2048
    __addr = "127.0.0.1"
    __time = 30
    __snapshots = 1000
    __system = ""

    """
        gets and sets
    """
    def __getsystem(self):
        return self.__system

    def __getsnapshots(self):
        return self.__snapshots
    
    def __gettime(self):
        return self.__time
    
    def __getport(self):
        return self.__port

    def __getaddr(self):
        return self.__addr;

    def __setsystem(self, s):
        self.__system = s

    def __settime(self, t):
        self.__time = t
        
    def __setport(self, p):
        self.__port = p

    def __setaddr(self, a):
        self.__addr = a

    def __setsnapshots(self, s):
        self.__snapshots = s

    """
        properties
    """
    Port = property(__getport, __setport)
    Address = property(__getaddr, __setaddr)
    TimeOut = property(__gettime, __settime)
    Snapshots = property(__getsnapshots, __setsnapshots)
    System = property(__getsystem, __setsystem)
    
    """
        utilities
    """
    @staticmethod
    def GetTime():
        return time.strftime("%I:%M:%S %p", time.localtime(time.time()))

    def PrintEvent(self, msg):
        if len(msg) > 0:
            print SimulatorServer.GetTime() + ": " + msg
            
    """
        constructor
    """
    def __init__(self):
        threading.Thread.__init__(self)

    """
        destructor
    """
    def __del__(self):
        pass
        #self.PrintEvent("Client Destructed.")

    def run(self):
        host = self.Address
        port = self.Port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.TimeOut)
        try:
            s.connect((host, port))
            if len(self.System) == 0:
                s.send('stop')
            else:
                s.send(self.System + ":" + str(self.Snapshots))
            data = s.recv(32)
            print host,':', port, 'says:', data    
        except socket.error:
            print host,':', port, 'is offline, stop '
        finally:
            s.close()

if __name__ == "__main__":
    totalsnapshots = 999
    machinelist = [
        ("127.0.0.1", 2048, "LTE"),
        ("192.168.2.123", 2048, "LTE")
#        ("192.168.2.124", 2048, "LTE")
    ]
    totalcnt = len(machinelist)
    avg = totalsnapshots / totalcnt
    start_time = time.time()
    threads = []
    for t in machinelist:
        at = SimulatorClient()
        at.Address = t[0]
        at.Port = t[1]
        at.System = t[2]
        at.Snapshots = avg
        threads.append(at)

    for t in threads:
        t.start()

    for t in threads:
        t.join()     
        
    print time.time() - start_time, "seconds"
    
    
        
        
    
