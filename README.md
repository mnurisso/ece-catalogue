## EC-EARTH4 AQUA catalogue

This repository contains a catalogue that can be opened by AQUA code for EC-Earth4 experiments on the HPC2020 machine at ECMWF.

The needed grids and fixes are now in the AQUA main.

Instructions:
-------------

- Install AQUA on HPC2020 following carefully the specific instructions in the [AQUA documentation](https://aqua.readthedocs.io/en/latest/installation.html#installation-on-ecmwf-hpc2020)

- If needed you can use the script ``install_aqua.sh`` to install AQUA in editable mode and add the hpc2020, epocal, obs catalogues

- Edit the file ``catalogs/hpc2020/machine.yaml`` setting appropriate paths where to store grids, areas and weights.

- If you need to download grids (If you keep the default for hpc2020 you do not need this)
  Then run the script ``install_grids.sh`` in this directory.

EC-Earth4 sources are now availble from the EC-EARTH4 model, your experiment identifier and one of the sources defined in the catalogue (such as ``monthly-atm``).

Next you can modify to your needs the job template in ``jobs/aqua_analysis_e486.job`` and run your first AQUA analysis.

Currently to add a new experiments you can use the catalogue generator in the ``catalog-generator`` folder.
