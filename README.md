## EC-EARTH4 AQUA catalogue

This repository contains a catalogue that can be opened by AQUA code for EC-Earth4 experiments on the HPC2020 machine at ECMWF.

The needed grids and fixes are now in the AQUA main.

Instructions:
-------------

- Install AQUA on your machine (e.g. HPC2020) following carefully the specific instructions in the [AQUA documentation](https://aqua.readthedocs.io/en/latest/installation.html)

- Install the catalogue in this repository in AQUA following the standard AQUA procedure. 
  The script ``install_aqua.sh`` summarizes all needed steps and installs AQUA in editable mode and adds the ece4-tuning, epochal, obs catalogues

- Edit the file ``catalogs/ece4-tuning/machine.yaml`` setting appropriate paths where to store grids, areas and weights or override these paths for your machine directly in the ``config-aqua.yaml`` file as [described in the documentation](https://aqua.readthedocs.io/en/latest/advanced_topics.html#set-up-the-configuration-file).

- If you need to download grids (If you keep the default for hpc2020 or you are running on
  a supported machine you probably do not need this), you can use the AQUA script 
  ``cli/grids-downloader/grids-downloader.sh`` to download them to the directory which you indicated in the previous step.

EC-Earth4 sources are now availble from the EC-EARTH4 model, your experiment identifier and one of the sources defined in the catalogue (such as ``monthly-atm``).

Next you can modify to your needs the job template in ``jobs/aqua_analysis.tmpl`` and run your first AQUA analysis.

To add a new experiment to the catalogue you can use the catalogue generator in the ``catalog-generator`` folder. Edit the `config.yaml` file in that directory to this end.

Please notice: there is currently an [issue](https://github.com/DestinE-Climate-DT/AQUA/issues/2011) in how AQUA processes dates in EC-Earth4 atmospheric output which requires the `center_time` option for timeseries and seasonal cycles to be se to false.
Please edit the files 

- `.aqua/diagnostics/timeseries/config_timeseries_atm.yaml`
-  `.aqua/diagnostics/timeseries/config_seasonalcycles_atm.yaml`
-  `.aqua/diagnostics/radiation/config_radiation-timeseries.yaml`
  
and set `center_time: false`

