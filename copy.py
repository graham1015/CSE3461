import sys, os

#gets filename from command line arguements
name = sys.argv[1];
dir = "recv/";

#make sub-directory if does not exist
if not os.path.exists(dir):
    os.makedirs(dir);
newFilename = dir+filename;

#opens the original file
try:
    original = open(filename,"rb");
except IOError as e:
    print ('The file with this filename does not exist.');

#creates/opens new file
newFile = open(newFilename,"wb+");

#loops and reads and writes 960 bytes at a time to new file
byte = originalFile.read(960);
while byte:
    newFile.write(byte);
    byte = originalFile.read(960);

#closes both files
newFile.close();
originalFile.close();




import sys, os

#get filename from arguments
filename = sys.argv[1];


#check if subdirectory exist, if not then create it
if not os.path.exist("recv/"):
    os.makedirs("recv/");

#open file in binary
try:
	file = open(filename, rb);
except IOError as e:
	print ('File does not exist.');
	
#create new file
newFile = open("recv/" + filename, "wb+");

#iterate through and copy bytes
section = file.read();
while section
