import sys, os

#get filename from arguments
fileName = sys.argv[1];


#check if subdirectory exist, if not then create it
if not os.path.exist("recv/"):
    os.makedirs("recv/");

#open file in binary
try:
	file = open(fileName, rb);
except IOError as e:
	print ("File does not exist.");
	
#create new file
newFile = open("recv/" + fileName, "wb+");

#iterate through and copy bytes
section = file.read(1000);
while section != b"":
	newFile.write(section);
	section = file.read(1000);

#close the files
file.close();
newFile.close();
