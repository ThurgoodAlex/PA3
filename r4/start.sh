#!/bin/bash
echo "Starting FRR..."
sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons
service frr restart
exec bash