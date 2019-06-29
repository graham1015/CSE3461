#Author : Gavin Graham


#Server Program
#Import Packages
import sys
import os
import socket

#Check to see if command line args are valid
if len(sys.argv) != 2:
	print('Invalid arguments. Use form: "ftps.py <remote-port>"');

#Set variable for port and host
HOST = socket.gethostname()
PORT = int(sys.argv[1])

try:
	cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print('Failed to create socket.')
	sys.exit();

print ('Socket Created') 

try:
	s.bind((HOST,PORT))
	print ('Socket bind complete')
except socket.error:
	print('Failed to bind socket to host')
	sys.exit()

print("Server is ready")

while True:
	data, addr = cliSocket.recvfrom(1000)
	print ('Recieving from' , addr)
	clientIP_encoded = data[0:4] 
	clientPORT_encoded = data[4:6] 
	if (int.from_bytes(data[6:7], byteorder='big') == 1): 
		sizeByte = data[7:len(data)] 
		size = int.from_bytes(byte_size, byteorder='big')
		print ('File size: ', size)
	if (int.from_bytes(data[6:7], byteorder='big') == 2): 
		filenameBytes = data[7:len(data)]
		filename = byte_filename.decode()
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
cliSocket.close()
print('File Successfully transfered. Connection closed.')