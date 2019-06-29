#Author : Gavin Graham


#Server Program
#Import Packages
import sys
import os
import socket

#Check to see if command line args are valid
if len(sys.argv) != 2:
	print('Invalid arguments. Use form: "ftps.py <remote-port>"')
	sys.exit()

#Set variable for port and host
HOST = socket.gethostname()
PORT = int(sys.argv[1])

try:
	servSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print('Failed to create socket.')
	sys.exit()

print ('Socket Created') 

try:
	servSocket.bind((HOST,PORT))
	print ('Socket bind complete')
except socket.error:
	print('Failed to bind socket to host')
	sys.exit()

print("Server is ready")

while 1:
	data, addr = servSocket.recvfrom(1000)
	print ('Recieving from' , addr)
	cliIP_encoded = data[0:4] 
	cliPORT_encoded = data[4:6] 
	if (int.from_bytes(data[6:7], byteorder='big') == 1): 
		sizeByte = data[7:len(data)] 
		size = int.from_bytes(sizeByte, byteorder='big')
		print ('File size: ', size)
	if (int.from_bytes(data[6:7], byteorder='big') == 2): 
		filenameBytes = data[7:len(data)]
		filename = filenameBytes.decode()
		filename = filename.lstrip()
		if not os.path.exists('recv/'):
			os.makedirs('recv/')
		file = open('recv/' + filename, 'wb')
	if (int.from_bytes(data[6:7], byteorder='big') == 3): 
		data = data[7:len(data)]
		file.write(data)
		if data == b"":
			break
	
file.close()
servSocket.close()
print('File Successfully transfered. Connection closed.')