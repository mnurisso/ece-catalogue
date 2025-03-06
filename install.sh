#!/bin/bash

# Simple script to install to AQUA
# This assumes that AQUA is already installed on your system

# Copy and link the files to the AQUA config directory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AQUA_DIR=~/.aqua

ln -s $SCRIPT_DIR/config/fixes/EC-EARTH4.yaml $AQUA_DIR/fixes/
ln -s $SCRIPT_DIR/config/grids/EC-EARTH4.yaml $AQUA_DIR/grids/

aqua add hpc2020 -e $SCRIPT_DIR/catalogs/hpc2020

dst=$(grep -A 2 '^hpc2020:' $SCRIPT_DIR/catalogs/hpc2020/machine.yaml|tail -1| sed -E 's/.*grids:\s*(.*)/\1/')
mkdir -p $dst/EC-EARTH4bis
cp $SCRIPT_DIR/grids/*.nc $dst/EC-EARTH4bis/

echo "Installation complete"
