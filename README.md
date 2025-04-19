To run my orchestrator, you first have to run './dockersetup'. Then you can run 'python3 Alex_Thurgood_u1350818.py --docker-build' and  'python3 Alex_Thurgood_u1350818.py --docker-up' and then 'sudo bash' .These commands set up the topology and installs frr and sets the inital weights for OSPF. 
After thats done, youll be able to run 'docker ps' to find the container names.
run 'python3 Alex_Thurgood_u1350818.py -h' to find the list of commands that can be run, but
 the option --add-routes, connects the Hosts to the network
 the option --north, sends the packts from  HostA through the path R1 -> R2 -> R3 to HostB
 the option --south, sends the packets from HostA thropugh the path R1 -> R4 -> R3 to HostB
