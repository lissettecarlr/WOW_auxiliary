from scapy.all import *
 
SYN=IP(dst="192.168.2.244")/TCP(dport=21,flags='S')
 
print ("-- Send SYN --")
#SYN.display()
 
print("\n\n-- SYN Received --")
response = sr1(SYN,timeout=1,verbose=0)
#response.display()
 
if int(response[TCP].flags) == 18:
    print("\n\n-- Sent ACK --")
    A = IP(dst="192.168.2.244")/TCP(dport=21,flags='A',ack=(response[TCP].seq+1))
    A.display()
    print("\n\n-- ACK Received --")
    response2 = sr1(A,timeout=1,verbose=0)
 #   response2.display()
else:
    print("SYN/ACK not returned")