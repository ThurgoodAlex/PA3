import subprocess
import argparse

hosts = {
    "pa3-ha-1": {"ip": "10.0.15.0/24", "gw": "10.0.14.4"},
    "pa3-hb-1": {"ip": "10.0.14.0/24", "gw": "10.0.15.4"},
}

def add_routes():
    # Add static routes from the hosts to the network
    for host, config in hosts.items():
        ip = config["ip"]
        gw = config["gw"]
        subprocess.run(f"docker exec -it {host} route add -net {ip} gw {gw}", shell=True, check=True)
    print("Host routes added successfully")



def get_eth_by_name(name, ip):
    # Get the ethernet interface name by IP address
    result = subprocess.run(f"docker exec -it {name} ip addr show | grep {ip}", shell=True, check=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        parts = line.split()
        ip_addr = parts[3] 
        if ip_addr.startswith(ip):
            return parts[1] 
    return None


def set_ospf_cost(name, interface, cost):
    # Set the OSPF cost for the specified interface
    subprocess.run(f"docker exec {name} vtysh "
        f"-c 'configure terminal' "
        f"-c 'interface {interface}' "
        f"-c 'ip ospf cost {cost}' "
        f"-c 'end' "
        f"-c 'write memory'",
        shell=True, check=True)

def ospf_north():
    # Set OSPF route to use R1 → R2 → R3
    set_ospf_cost("pa3-r1-1", "10.0.10.4", 2)   # R1 → R2
    set_ospf_cost("pa3-r1-1", "10.0.13.4", 50)  # R1 → R4
    set_ospf_cost("pa3-r2-1", "10.0.11.3", 2)   # R2 → R3
    set_ospf_cost("pa3-r4-1", "10.0.12.4", 50)  # R4 → R3
    set_ospf_cost("pa3-r3-1", "10.0.11.4", 2)   # R3 ← R2 (north path)
    print("Changed to northern path")


def ospf_south():
    # Set OSPF route to use R1 → R4 → R3
    set_ospf_cost("pa3-r1-1", "10.0.10.4", 50)
    set_ospf_cost("pa3-r1-1", "10.0.13.4", 2)
    set_ospf_cost("pa3-r2-1", "10.0.11.3", 50)
    set_ospf_cost("pa3-r4-1", "10.0.12.4", 2)
    set_ospf_cost("pa3-r3-1", "10.0.11.4", 50)
    set_ospf_cost("pa3-r3-1", "10.0.12.3", 2)
    print("Changed to southern path")

def docker_build():
    # Build the docker containers
    # This installs frr, sets the original ospf weights and the network topology.
    subprocess.run("docker compose build", shell=True, check=True)
    print("Docker containers built successfully")


def docker_up():
    # Start the docker containers
    subprocess.run("docker compose up -d", shell=True, check=True)
    print("Docker containers built successfully")

if __name__ == "__main__":
    # Create the argument parser
    # This allows the user to specify which function to run from the command line.
    parser = argparse.ArgumentParser()

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
    parser.add_argument(
        "--docker-build",
        action="store_true",
        help="Build the docker containers. This installs frr, sets the original ospf weights and the network topology."
    )
    parser.add_argument(
        "--docker-up",
        action="store_true",
        help="Start the docker containers."
    )
    args = parser.parse_args()

    if args.add_routes:
        add_routes()
    elif args.north:
        ospf_north()
    elif args.south:
        ospf_south() 
    elif args.docker_build:
        docker_build()
    elif args.docker_up:
        docker_up()
    else:
        parser.print_help()