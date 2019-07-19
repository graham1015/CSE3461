CSE3461 - Champion MWR 2:20-3:45
Name : Gavin Graham
.# : graham.1015
To run program type:

  On System-2/Server (Where the file is to be sent)
  python3 ftps.py <local-port-on-System-2>
  
  
  On System-1/client (Where the file originates)
	  Run the troll 
	  	troll -C <System 1 IP> -S <System 2 IP> -a 4567 -b <server port on system 2> -r -t -x 0 <troll port on system 2>

	  Finally open a new window and run this program	
  		python3 ftpc.py <System 2 IP> <server port on system 2> <file to transfer>

* port 4567 is the hardcoded client port