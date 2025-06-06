#!/bin/bash

# Simple script to setup AQUA and install catalogs
# This assumes that AQUA is already installed on your system

set -e

# Check if AQUA is set and the file exists
if [[ -z "$AQUA" ]]; then
    echo -e "\033[0;31mWarning: The AQUA environment variable is not defined."
    echo -e "\033[0;31mWarning: We are assuming AQUA is installed in your HPCPERM, i.e. $HPCPERM/AQUA"
    echo -e "\x1b[38;2;255;165;0mAlternatively, define the AQUA environment variable with the path to your 'AQUA' directory."
    echo -e "For example: export AQUA=/path/to/aqua\033[0m"
    AQUA=$HPCPERM/AQUA
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AQUA_DIR=~/.aqua
MACHINE=hpc2020

# Copy and link the files to the AQUA config directory
aqua install $MACHINE -e $AQUA/config 
aqua add epochal -e $SCRIPT_DIR/catalogs/epochal
aqua add hpc2020 -e $SCRIPT_DIR/catalogs/hpc2020

# Add observations.
# If you have separately cloned the ClimateDT catalogue (https://github.com/DestinE-Climate-DT/Climate-DT-catalog) 
# then use "aqua add obs -e $DIR_OF_YOUR_CATALOGUE/catalogs/obs
aqua add obs

echo "Installation complete"
