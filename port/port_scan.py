# from scapy.all import *
 
# SYN=IP(dst="192.168.2.217")/TCP(dport=22,flags='S')
 
# print ("-- Send SYN --")
# #SYN.display()
 
# print("\n\n-- SYN Received --")
# response = sr1(SYN,timeout=0.5,verbose=0)
# # response.display()
# print(response)
 
# if int(response[TCP].flags) == 18:
#     print("\n\n-- Sent ACK --")
#     A = IP(dst="192.168.2.244")/TCP(dport=21,flags='A',ack=(response[TCP].seq+1))
#     A.display()
#     print("\n\n-- ACK Received --")
#     response2 = sr1(A,timeout=1,verbose=0)
#  #   response2.display()
# else:
#     print("SYN/ACK not returned")

from scapy.all import *
def port_scan(port):
    answer= sr1(IP(dst="47.108.178.9") / (TCP(dport=int(port), flags="S")),timeout=0.1,verbose=0)
    if answer == None:
        # print(port,"not ack")
        pass
    else:
        if answer[TCP].flags == 18:
            print(port,"is Open")
        if answer[TCP].flags == 20:
            print(port,"is Closed")

for i in range(6000):        
    port_scan(i)
