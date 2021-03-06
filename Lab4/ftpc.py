#Author : Gavin Graham

#Client Program
#Import Packages
import socket
import sys
import os
import time
import select

#Check to see if command line args are valid
if len(sys.argv) != 5:
	print('Invalid arguments. Use form: "ftpc.py <IP-address-of-System-2> <remote-port-on-System-2> <troll-port-on-System-1> <local-file-to-transfer>"')

HOST = sys.argv[1]
PORT = int(sys.argv[2])
TROLL = int(sys.argv[3])
FILENAME = sys.argv[4]

#Create connection
try:
	cliSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except (socket.error):
	print('Failed to create socket.')
	sys.exit();

cliSocket.bind((socket.gethostname(),4567))

print ('Socket Created') 

# Check if file exists
if not os.path.exists(FILENAME):
	print ('Error: Enter valid filename.')

#get size of file
size = os.path.getsize(FILENAME)

#prep size, filename, IP, and port to be sent
hostIP = socket.gethostbyname(socket.getfqdn(HOST))
sizeBytes = size.to_bytes(4, byteorder = 'big')
correctedFILENAME = FILENAME.rjust(20)
filenameBytes = correctedFILENAME.encode(encoding="ascii")
hostBytes = socket.inet_aton(hostIP) 
portBytes = PORT.to_bytes(2, byteorder='big') 

#open file to read binary
file = open(FILENAME, 'rb') 

#Set flags and send size and filename
flag = 1	
flagBytes = flag.to_bytes(1, byteorder = 'big') 

#set ack variables
ack = 0
ackNum = -1
ackBytes = ack.to_bytes(1, byteorder = 'big')

#while notacked
while ack != ackNum:
	try:
		cliSocket.sendto(hostBytes+portBytes+flagBytes+ackBytes+sizeBytes,('', TROLL))
	except (socket.error, msg):
		print('Failed to send size of file to TROLL: '+ str(msg[0]) + ' , Error message: ' + msg[1])
		sys.exit()
	rlist, wlist, xlist = select.select([cliSocket], [], [], .05)
	if len(rlist) > 0:
		# socket has recived some data
		ackRead = rlist[0].recv(1000)
		ackBytes= ackRead[7:8]
		ackNum = int.from_bytes(ackBytes, byteorder = 'big')
	if [rlist, wlist, xlist] == [ [], [], [] ]: # if packet not ACKed then timeout.
		print("Timeout")
	
print ('Size sent')


flag = 2
flagBytes = flag.to_bytes(1, byteorder = 'big') 

ack = ack + 1
ackBytes = ack.to_bytes(1, byteorder = 'big')

#while not acked
while ack != ackNum:
	try:
		cliSocket.sendto(hostBytes+portBytes+flagBytes+ackBytes+filenameBytes,('', TROLL))
	except (socket.error, msg):
		print('Failed to send name of file to TROLL: '+ str(msg[0]) + ' , Error message: ' + msg[1])
		sys.exit()
	rlist, wlist, xlist = select.select([cliSocket], [], [], .05)
	if len(rlist) > 0:
		# socket has recived some data
		ackRead = rlist[0].recv(1000)
		ackBytes= ackRead[6:]
		ackNum = int.from_bytes(ackBytes, byteorder = 'big')
	if [rlist, wlist, xlist] == [ [], [], [] ]: # if packet not ACKed then timeout.
		print("Timeout")
	
print ('filename sent')


flag = 3
flagBytes = flag.to_bytes(1, byteorder = 'big') 

#read and send data of file
data = file.read(1000)
while data != b"":
	ack = ack + 1
	ack = ack % 2
	ackBytes = ack.to_bytes(1, byteorder = 'big')
	while ack != ackNum:
		try:
			cliSocket.sendto(hostBytes+portBytes+flagBytes+ackBytes+data,('', TROLL))
		except (socket.error, msg):
			sys.exit()
		rlist, wlist, xlist = select.select([cliSocket], [], [], .05)
		if len(rlist) > 0:
			# socket has recived some data
			ackRead = rlist[0].recv(1000)
			ackBytes= ackRead[6:]
			ackNum = int.from_bytes(ackBytes, byteorder = 'big')
			time.sleep(.01)		
		if [rlist, wlist, xlist] == [ [], [], [] ]: # if packet not ACKed then timeout.
			print("Timeout")
	data = file.read(1000)
cliSocket.sendto(hostBytes+portBytes+flagBytes+ackBytes+data,('', TROLL)) 

file.close()
cliSocket.close()

print('File Successfully transfered. Connection closed.')
