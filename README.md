To run my orchestrator, you first have to run './dockersetup'. You may have to run the command 'chmod +x dockersetup' before running it after running this you may also need to run 'sudo bash'. 
Then you can run 'python3 Alex_Thurgood_u1350818.py --docker-build' and  'python3 Alex_Thurgood_u1350818.py --docker-up' and then 'sudo bash' .These commands set up the topology and installs frr and sets the inital weights for OSPF. 
After that's done, you'll be able to run 'docker ps' to find the container names.

run 'python3 Alex_Thurgood_u1350818.py -h' to find the list of commands that can be run, but
   --add-routes, connects the Hosts to the network
   --north, sends the packets from  HostA through the path R1 -> R2 -> R3 to HostB
   --south, sends the packets from HostA through the path R1 -> R4 -> R3 to HostB
