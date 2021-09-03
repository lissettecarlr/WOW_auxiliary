from bluepy import btle

print("Connecting...")
dev = btle.Peripheral("B0:B4:48:BF:C9:83")
 
print("Services...")
for svc in dev.services:
    print(str(svc))