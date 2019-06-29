#Author : Gavin Graham

#Client Program
#Import Packages
import socket
import sys
import os
import time

#Check to see if command line args are valid
if len(sys.argv) != 5:
	print('Invalid arguments. Use form: "ftpc.py <remote-IP> <remote-port> <troll-port> <local-file>"')

HOST = sys.argv[1]
PORT = int(sys.argv[2])
TROLL = int(sys.argv[3])
FILENAME = sys.argv[4]

#Create connection
try:
	cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
sizeBytes = size.to_bytes(4, byteorder = 'big')
correctedFILENAME = FILENAME.rjust(20)
filenameBytes = correctedFILENAME.encode(encoding="ascii")
hostBytes = socket.inet_aton(HOST) 
portBytes = PORT.to_bytes(2, byteorder='big') 

#open file to read binary
file = open(FILENAME, 'rb') 

#Set flags and send size and filename
flag = 1	
flagBytes = flag.to_bytes(1, byteorder = 'big') 

cliSocket.sendto(hostBytes+portBytes+flagBytes+sizeBytes,('', TROLL))
print ('Size sent')

flag = 2
flagBytes = flag.to_bytes(1, byteorder = 'big') 

cliSocket.sendto(hostBytes+portBytes+flagBytes+filenameBytes,('', TROLL))
print ('Name sent')

flag = 3
flagBytes = flag.to_bytes(1, byteorder = 'big') 

#read and send data of file
data = file.read(1000)
while data:
	cliSocket.sendto(hostBytes+portBytes+flagBytes+data,('', TROLL)) 
	data = file.read(1000)
	time.sleep(.01)
cliSocket.sendto(hostBytes+portBytes+flagBytes+data,('', TROLL)) 

file.close()
cliSocket.close()

print('File Successfully transfered. Connection closed.')
