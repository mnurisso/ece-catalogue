#!/bin/bash

# Simple script to install grids for AQUA
# This assumes that AQUA is already installed on your system

# Before running this script edit the files .aqua/catalogs/hpc2020/machine.yaml
# and the file .aqua/catalogs/hpc2020/machine.yaml  indicating the correct 
# location for grids, weights, areas

set -e

AQUA_DIR=~/.aqua

# Download grids from DKRZ Swift
# Figure out from the machine file where to store the grid data
dst=$(grep -A 2 '^hpc2020:' $AQUA_DIR/catalogs/hpc2020/machine.yaml|tail -1| sed -E 's/.*grids:\s*(.*)/\1/')
mkdir -p $dst/EC-EARTH4
cd $dst
wget "https://swift.dkrz.de/v1/dkrz_a973e394-5f24-4f4d-8bbf-1a83bd387ccb/AQUA/grids/EC-EARTH4.tar.gz?temp_url_sig=46efc8c2277242713a7999f8b6fb2d49fb340b91&temp_url_expires=2027-02-04T17:04:56Z" -O EC-EARTH4.tar.gz
tar xvfz EC-EARTH4.tar.gz
rm EC-EARTH4.tar.gz

echo "Installation of grids complete"
