#!/bin/bash

# Simple script to install to AQUA
# This assumes that AQUA is already installed on your system

# Copy and link the files to the AQUA config directory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AQUA_DIR=~/.aqua

aqua grids add -e $SCRIPT_DIR/config/grids/EC-EARTH4.yaml
aqua fixes add -e $SCRIPT_DIR/config/fixes/EC-EARTH4.yaml
aqua add hpc2020 -e $SCRIPT_DIR/catalogs/hpc2020
# aqua add epochal -e $SCRIPT_DIR/catalogs/epochal

# Download grids from DKRZ Swift
dst=$(grep -A 2 '^hpc2020:' $AQUA_DIR/catalogs/hpc2020/machine.yaml|tail -1| sed -E 's/.*grids:\s*(.*)/\1/')
mkdir -p $dst/EC-EARTH4
cd $dst
wget "https://swift.dkrz.de/v1/dkrz_a973e394-5f24-4f4d-8bbf-1a83bd387ccb/AQUA/grids/EC-EARTH4.tar.gz?temp_url_sig=46efc8c2277242713a7999f8b6fb2d49fb340b91&temp_url_expires=2027-02-04T17:04:56Z" -O EC-EARTH4.tar.gz
tar xvfz EC-EARTH4.tar.gz
rm EC-EARTH4.tar.gz

echo "Installation complete"