import subprocess
import os

routers = {
    "R1":{
        "container_name": "part1-r1-1",
        "interfaces":{
            "eth0":"10.0.14.4/24", # R1 to host A
            "eth1":"10.0.10.4/24", # R1 to R2
            "eth2": "10.0.13.4/24", # R1 to R4
        }
    },
    "R2":{
        "container_name": "part1-r2-1",
        "interfaces":{
                "eth0":"10.0.10.3/24", # R2 to R1
                "eth1":"10.0.11.3/24", # R2 to R3

        }
    },
    "R3":{
        "container_name": "part1-r3-1",
        "interfaces":{
                "eth0":"10.0.11.4/24", # R3 to R2
                "eth1":"10.0.12.3/24", # R3 to R4
                "eth2":"10.0.15.4/24", # R3 to host B

            }
    },

    "R4":{
        "container_name": "part1-r4-1",
        "interfaces":{
                "eth0":"10.0.13.4/24", # R4 to R1
                "eth1":"10.0.12.4/24", # R4 to R3

            }
    },
}

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


#show ip ospf interface in vtysh and copy that into a new one that paste into dockerfile or python script

if __name__ == "__main__":
    add_routes()
