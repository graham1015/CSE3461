#Author : Gavin Graham


#Server Program
#Import Packages
import sys
import os
import socket

#Check to see if command line args are valid
if len(sys.argv) != 3:
	print('Invalid arguments. Use form: "ftps.py <local-port-on-System-2> <troll-port-on-System-2>"')
	sys.exit()

#Set variable for port and host
HOST = socket.gethostname()
PORT = int(sys.argv[1])
TROLL = int(sys.argv[2])

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

bytesRead = 0
dataDup = b""

while 1:
	data, addr = servSocket.recvfrom(1000)
	cliIP_encoded = data[0:4] 
	cliPORT_encoded = data[4:6]
	cliACK_encoded = data[7:8]
	if data == dataDup:
		servSocket.sendto(cliIP_encoded+cliPORT_encoded+cliACK_encoded, ("", TROLL))
		print ("Duplicate Packet")
	else:
		dataDup = data
		servSocket.sendto(cliIP_encoded+cliPORT_encoded+cliACK_encoded, ("", TROLL))
		if (int.from_bytes(data[6:7], byteorder='big') == 1): 
			sizeByte = data[8:len(data)] 
			print ('Recieving from' , addr)
			size = int.from_bytes(sizeByte, byteorder='big')
			print ('File size: ', size)
		if (int.from_bytes(data[6:7], byteorder='big') == 2): 
			filenameBytes = data[8:len(data)]
			filename = filenameBytes.decode()
			filename = filename.lstrip()
			if not os.path.exists('recv/'):
				os.makedirs('recv/')
			file = open('recv/' + filename, 'wb')
			print ('File name: ', filename)
		if (int.from_bytes(data[6:7], byteorder='big') == 3): 
			data = data[8:len(data)]
			file.write(data)
			if len(data) < 1000:
				break
	
file.close()
servSocket.close()
print('File Successfully transfered. Connection closed.')
