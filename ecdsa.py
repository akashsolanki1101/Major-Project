
import ecdsa
import random
import libnum
import hashlib
import sys
import re

def GetKey():
	G = ecdsa.NIST256p.generator
	order = G.order()
	priv = random.randrange(1,order)
	Public_key = ecdsa.ecdsa.Public_key(G,G* priv)
	Public_key = re.search(r'(0x)(.{16})', str(Public_key))
	
	return str(Public_key.group(0))
	# Public_key = ecdsa.ecdsa.Public_key(G, G * priv)
	# Private_key = ecdsa.ecdsa.Private_key(Public_key, priv)
	# Private_key = re.search(r'(0x)(.{16})', str(Private_key))
	# print(Public_key.group(0), Private_key.group(0))

file = open('./Credentials/keys.txt','w')
for i in range(0,20):
	file.write(GetKey()+"\n")
	
file.close()