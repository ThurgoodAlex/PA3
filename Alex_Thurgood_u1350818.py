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


def ospf_north():
    # Set OSPF route to use R1 → R2 → R3
    subprocess.run("docker exec -it pa3-r1-1 vtysh -c 'configure terminal' -c 'interface eth1' -c 'ip ospf cost 20' -c 'end'", shell=True, check=True)
    subprocess.run("docker exec -it pa3-r1-1 vtysh -c 'configure terminal' -c 'interface eth2' -c 'ip ospf cost 2' -c 'end'", shell=True, check=True)
    subprocess.run("docker exec -it pa3-r1-1 vtysh -c 'write memory'", shell=True, check=True)

    print("Changed to northern path")


def ospf_south():
    # Set OSPF route to use R1 → R4 → R3
    subprocess.run("docker exec -it pa3-r1-1 vtysh -c 'configure terminal' -c 'interface eth1' -c 'ip ospf cost 2' -c 'end'", shell=True, check=True)
    subprocess.run("docker exec -it pa3-r1-1 vtysh -c 'configure terminal' -c 'interface eth2' -c 'ip ospf cost 20' -c 'end'", shell=True, check=True)
    subprocess.run("docker exec -it pa3-r1-1 vtysh -c 'write memory'", shell=True, check=True)
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

