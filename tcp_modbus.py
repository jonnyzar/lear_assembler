#!/usr/bin/env python3

'''
Modbus client

establish TCP
send Modbus payload
'''


from scapy.all import *
from scapy.contrib.modbus import *
import random
import time


class TCP_IP_connection:

    def __init__(self, destIP, srcP, destP):
        
        self.scrPort = srcP
        self.destPort = destP        
        self.ip = IP(dst=destIP)
   
    def openTCPconn(self):
        '''
        Create TCP connection and return the scapy packet
        '''
        
        #perform TCP handshake         
        
        #SYN 
        syn_tcp = TCP (sport=self.scrPort, dport = self.destPort,\
         flags='S')         
        syn_pkt = self.ip/syn_tcp         
        
        #send SYN packets until SYN-ACK received      
        psync = sr1(syn_pkt, timeout=1)        

        tcp = TCP (sport=self.scrPort, dport = self.destPort,\
        flags='A')   
        ack_pkt = self.ip/tcp     
        pack = sr1(ack_pkt, timeout=1)         

        
    def killTCPconn (self):
        '''
        terminate active TCP connection
        '''
        fin_tcp = TCP (sport=self.scrPort, dport = self.destPort,\
        flags='RA')
        send(self.ip/fin_tcp)                
          
    def sendPayload (self, payload):      
        #construct TCP packet
        out_tcp = TCP (sport=self.scrPort, dport = self.destPort,\
             flags=0x018)  
        
        out_packet = self.ip/out_tcp/payload
        p_sent = sr1(out_packet, timeout=1)

 

def main():
    
    destIP = '192.168.178.24' 
    srcP = 65001
    destP = 502 
    
    modbusTCP = TCP_IP_connection(destIP, srcP, destP) 
    modbusTCP.openTCPconn()   
    
    modADU = ModbusADURequest(transId=1,  protoId=0,len=None, unitId=1)
    modReq = ModbusPDU01ReadCoilsRequest (funcCode = 1, startAddr =0, quantity=5)
    modload = modADU/modReq
    modbusTCP.sendPayload(modload)
    
    modbusTCP.killTCPconn() 
    #modbusTCP.pkt.show()

if __name__=="__main__":
    main()
