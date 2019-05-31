#Author: Gavin Graham

#Server Program
#Import Packages
import sys
import os
import socket



#Check to see if command line args are valid
if len(sys.argv) != 2:
	print('Invalid arguments. Use form: "Ftps.py <remote-port>"');

#Set variable for port and host
HOST = '';
PORT = int(sys.argv[1]);



#Open the socket and confirm when open
servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
servSocket.bind(HOST, PORT);
print("Server is ready");

#Connect with client
servSocket.listen(1);
connSock, addr = servSocket.accept();
print ('Connected with ', addr);

#First 4 bytes indicate the file size
byteSize = connSock.recv(4);
size = int.from_bytes(byteSize, byteorder='big');
print ('File size: ', size);

#The following 20 bytes indicate file name
nameByte= connSock.recv(20);
name = nameByte.decode().lstrip();
print ('File name: ', name);

#create subDirectory if does not exist
folder = "recv/";
if not os.path.exists(folder):
		os.mkdir(folder);
fileName = folder+name;

#Open file
file = open(fileName, 'wb+');

#Read packets 1000 bytes at a time until the entire message is read. Then write to new file.
bytesRead = 0;
while bytesRead < size:
	data = connSock.recv(1000)
	bytesRead += len(data)
	file.write(data)


#Close file and connection
file.close();
connSock.close();
print('File Successfully transfered. Connection closed.')
