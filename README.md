## EC-EARTH4 AQUA catalogue

This repository contains a catalogue that can be opened by AQUA code for EC-Earth4 experiments on the HPC2020 machine at ECMWF.

It also provides needed grids and fixes.

Instructions:
-------------

- Edit the file ``catalogs/hpc2020/machine.yaml`` setting appropriate paths where to store grids, areas and weights.
- Then run the script ``install.sh`` in this directory.

EC-Earth4 sources are now availble from the EC-Earth4 mode, your experiment identifier and one of the sources defined in the catalogue (such as ``monthly-atm``).


