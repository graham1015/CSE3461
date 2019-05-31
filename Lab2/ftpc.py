#Author: Gavin Graham

#Client Program
#Import Packages
import sys
import os
import socket

#Check to see if command line args are valid
if len(sys.argv) != 4:
	print('Invalid arguments. Use form: "ftpc.py <remote-IP> <remote-port> <local-file>"');

#Set variable for port, host, and filename
HOST = sys.argv[1];
PORT = int(sys.argv[2]);
FILENAME = sys.argv[3];


cliSocket = socket(socket.AF_INET, socket.SOCKSTREAM);


cliSocket.connect(HOST, PORT);
print ('Connected with ', Host, ' on port ', str(PORT));


# Check if file exists
if not os.path.exists(FILENAME):
	print ('Error: Enter valid filename.');

#get size of file
size = os.path.getsize(FILENAME);

#prep size and filename to be sent
sizeBytes = size.to_bytes(4, byteorder = 'big');
correctedFILENAME = FILENAME.rjust(20);  
filenameBytes = correctedFILENAME.encode(encoding="ascii");

#send size
cliSocket.send(sizeBytes);
print ('Size sent');

#send filename
cliSocket.send(filenameBytes);
print ('Name sent');

#open file
file = open(FILENAME, 'rb');

#Read data and send in 1000 byte packets
data = file.read(1000);
while data:
	cliSocket.send(data); 
	data = file.read(1000);

#close file and connection
file.close();
cliSocket.close();
print('File Successfully transfered. Connection closed.')
