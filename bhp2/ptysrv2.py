# Copyright (c) Twisted Matrix Laboratories
# See LICENSE for details

"""
A PTY server that spawns a shell upon connection.

Run this example by typing in:
> python ptyserv.py

Telnet to the server once you start it by typing in: 
> telnet localhost 5823
"""
from __future__ import print_function

from twisted.internet import reactor, protocol, epollreactor
from twisted.internet.epollreactor import EPollReactor
from threading import Thread
import os
class ptySrv(Thread):
    class FakeTelnet(protocol.Protocol):
        # t = Thread(target = )
        commandToRun = ['/bin/sh'] # could have args too
        dirToRunIn = '/tmp'
        print('[+] listening for connection')
        def connectionMade(self):
            print('[+] connection received')
            self.propro = ptySrv.ProcessProtocol(self)
            reactor.spawnProcess(self.propro, self.commandToRun[0], self.commandToRun, {}, self.dirToRunIn, usePTY=1)
            
        def dataReceived(self, data):
            self.propro.transport.write(data)
        def connectionLost(self, reason):
            print('[-] connection lost')
            self.propro.transport.loseConnection()


    class ProcessProtocol(protocol.ProcessProtocol):

        def __init__(self, pr):
            self.pr = pr

        def outReceived(self, data):
            self.pr.transport.write(data)
        
        def processEnded(self, reason):
            print('[-] protocol connection lost')
            # print('debug reason: %s' % reason)
            self.pr.transport.loseConnection()
            reactor.stop()

        def errReceived(self, data):
            print('errors received: %s' & data)

# f = protocol.Factory()
# f.protocol = ptySrv.FakeTelnet
# reactor.listenTCP(5823, f)
# reactor.run()
def main():
    # self = EPollReactor()
    # f = protocol.Factory()
    # epollreactor.EPollReactor.spawnProcess = ptySrv.FakeTelnet
    # reactor.listenSSL(self, 5823, f)
    # reactor.run()
    f = protocol.Factory()
    f.protocol = ptySrv.FakeTelnet
    reactor.listenTCP(5823, f)
    reactor.run(installSignalHandlers=True)

if __name__ == '__main__':
    main()  