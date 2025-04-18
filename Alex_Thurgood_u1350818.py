import subprocess
import os
import argparse

# routers = {
#     "R1":{
#         "container_name": "part1-r1-1",
#         "interfaces":{
#             "eth0":"10.0.14.4/24", # R1 to host A
#             "eth1":"10.0.10.4/24", # R1 to R2
#             "eth2": "10.0.13.4/24", # R1 to R4
#         }
#     },
#     "R2":{
#         "container_name": "part1-r2-1",
#         "interfaces":{
#                 "eth0":"10.0.10.3/24", # R2 to R1
#                 "eth1":"10.0.11.3/24", # R2 to R3

#         }
#     },
#     "R3":{
#         "container_name": "part1-r3-1",
#         "interfaces":{
#                 "eth0":"10.0.11.4/24", # R3 to R2
#                 "eth1":"10.0.12.3/24", # R3 to R4
#                 "eth2":"10.0.15.4/24", # R3 to host B

#             }
#     },

#     "R4":{
#         "container_name": "part1-r4-1",
#         "interfaces":{
#                 "eth0":"10.0.13.4/24", # R4 to R1
#                 "eth1":"10.0.12.4/24", # R4 to R3

#             }
#     },
# }

hosts = {
    "pa3-ha-1": {"ip": "10.0.15.0/24", "gw": "10.0.14.4"},
    "pa3-hb-1": {"ip": "10.0.14.0/24", "gw": "10.0.15.4"},
}

def add_routes():
    for host, config in hosts.items():
        ip = config["ip"]
        gw = config["gw"]
        subprocess.run(f"docker exec -it {host} route add -net {ip} gw {gw}", shell=True, check=True)
    print("Host routes added successfully")


def ospf_north():
    subprocess.run(f"docker exec -it pa3-r1-1 vtysh -c 'configure terminal' -c 'interface eth2' -c 'ip ospf cost 2' -c 'end'", shell=True, check=True)
    subprocess.run(f"docker exec -it pa3-r1-1 vtysh -c 'write memory'", shell=True, check=True)
    print("Changed to northern path")


def ospf_south():
    subprocess.run(f"docker exec -it pa3-r1-1 vtysh -c 'configure terminal' -c 'interface eth2' -c 'ip ospf cost 20' -c 'end'", shell=True, check=True)
    subprocess.run(f"docker exec -it pa3-r1-1 vtysh -c 'write memory'", shell=True, check=True)
    print("Changed to southern path")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="run -add-routes to add the routes from the hosts to the network. run -north to change the path to R -> R2 -> R3 and run -south to change the path to R1 -> R4 -> R3")
    parser.add_argument(
        "--add-routes",
        action="store_true",
        help="Add static routes from the hosts to the network."
    )

    parser.add_argument(
        "--north",
        action="store_true",
        help="Set OSPF route to use R1 → R2 → R3"
    )
    parser.add_argument(
        "--south",
        action="store_true",
        help="Set OSPF route to use R1 → R4 → R3"
    )
    args = parser.parse_args()

    if args.add_routes:
        add_routes()
    else:
        parser.print_help()

