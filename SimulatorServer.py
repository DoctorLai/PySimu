#!/usr/bin/env python
"""
    SimulatorServer.py
    Server Socket
    zhihua.lai@ranplan.co.uk
"""

import time
import socket
import threading
from sys import *

class SimulatorServer(threading.Thread):
    """
        Simulator Socket Server
    """

    """
        private attributes
    """
    __maxc = 32
    __port = 2048
    __addr = ""
    __running = False

    """
        gets and sets
    """
    def __getmaxc(self):
        return self.__maxc

    def __getport(self):
        return self.__port

    def __getaddr(self):
        return self.__addr;

    def __setmaxc(self, c):
        self.__addr = c

    def __setport(self, p):
        self.__port = p

    def __setaddr(self, a):
        self.__addr = a

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
        properties
    """
    MaxConnections = property(__getmaxc, __setmaxc)
    Port = property(__getport, __setport)
    Address = property(__getaddr, __setaddr)

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
        #self.PrintEvent("Server Destructed.")

    """
        start listening
    """
    def run(self):
        self.PrintEvent("Start Listening on " + self.Address + ":" + str(self.Port))
        svr = None
        self.__running = True
        try:
            svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            svr.bind((self.Address, self.Port))
            svr.listen(1)
            while self.__running:
                self.PrintEvent("Listening...")
                conn, addr = svr.accept()
                data = conn.recv(32)
                if len(data) > 0:
                    (system, snapshots) = data.split(':')
                    if snapshots.isdigit() and (len(system) > 0):
                        snapshots = int(snapshots)
                        if snapshots > 0:
                            import SimulatorTest
                            SimulatorTest.launch(system, snapshots)
                            conn.send(str(snapshots) + " snapshots finished.")
                        else:
                            self.PrintEvent("Ignored: snapshots = 0")
                    elif data == "stop":
                        self.Stop()
                        break
                    else:
                        self.PrintEvent("Unknown Commands Received: " + data)
                else:
                    pass
        except socket.error, (value, msg):
            if svr:
                svr.close()
            self.PrintEvent("Could Not Open Socket: " + msg)
        finally:
            if svr:
                svr.close()

    """
        stop the server
    """
    def Stop(self):
        if self.__running:
            self.PrintEvent("Stopping Server..")
            self.__running = False

if __name__ == "__main__":
    svr = SimulatorServer()
    if len(argv) > 1:
        svr.Address = argv[1]
    if len(argv) > 2:
        if argv[2].isdigit():
            svr.Port = int(argv[2])
    svr.start()

    
    
