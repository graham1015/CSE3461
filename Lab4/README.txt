CSE3461 - Champion MWR 2:20-3:45
Name : Gavin Graham
.# : graham.1015
To run program type:

  On System-2/Server (Where the file is to be sent)
  python3 ftps.py <local-port-on-System-2> <troll-port-on-System-2>
  
  
  On System-1/client (Where the file originates)
	  Run the troll 
	  	troll -C <IP-address-of-System-1> -S <IP-address-of-System-2> -a <client-port-on-System-1> -b <server-port-on-System-2> <troll-port-on-System-1> -t -x <packet-drop-%>


  On System-2/Server (Where the file is to be sent)
     Run
  		troll -C <IP-address-of-System-2> -S <IP-address-of-System-1> -a <server-port-on-System-2> -b <client-port-on-System-1> <troll-port-on-System-2> -t -x <packet-drop-%>


  Finally open a new window and run this program	
  		python3 ftpc.py <IP-address-of-System-2> <remote-port-on-System-2> <troll-port-on-System-1> <local-file-to-transfer>