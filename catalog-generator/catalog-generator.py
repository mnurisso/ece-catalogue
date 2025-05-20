#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Tool for generating catalog entries for the EC-EARTH4 model based on jinja
Based on the AQUA catalog generator
'''

import os
import sys
import argparse
import jinja2

from aqua import Reader, inspect_catalog
from aqua.util import ConfigPath, load_yaml, dump_yaml, get_arg
from aqua.logger import log_configure


def parse_arguments(arguments):
    """
    Parse command line arguments for the LRA CLI
    """

    parser = argparse.ArgumentParser(description='EC-EARTH entries generator')

    parser.add_argument('-a', '--amip', action='store_true', help='AMIP run')
    parser.add_argument('-c', '--config', type=str,
                        help='yaml configuration file')
    parser.add_argument('-d', '--description', type=str,
                        help='description')
    parser.add_argument('-m', '--model', type=str,
                        help='model name')
    parser.add_argument('-e', '--exp', type=str,
                        help='experiment name')
    parser.add_argument('-j', '--jinja', type=str,
                        help='jinja template file')
    parser.add_argument('-l', '--loglevel', type=str,
                        help='loglevel', default='INFO')

    return parser.parse_args(arguments)


if __name__ == '__main__':

    # Parse arguments
    args = parse_arguments(sys.argv[1:])
    definitions_file = get_arg(args, 'config', 'config.yaml')
    jinja_file = get_arg(args, 'jinja', 'ec-earth.j2')
    loglevel = get_arg(args, 'loglevel', 'WARNING')

    if not jinja_file:
        raise FileNotFoundError('You need to specify a jinja file for templating')

    logger = log_configure(loglevel, 'EC-EARTH catalog generator')

    definitions = load_yaml(definitions_file)

    model = get_arg(args, 'model', None)
    if model:
        definitions['model'] = model

    exp = get_arg(args, 'exp', None)
    if exp:
        definitions['exp'] = exp
        definitions['exp_name'] = exp

    amip = get_arg(args, 'amip', None)
    if amip:
        definitions['amip'] = amip

    description = get_arg(args, 'description', None)
    if description:
        definitions['description'] = description

    # Check if all mandatory fields are present
    if 'freq' not in definitions:
        definitions['freq'] = 'monthly'
        logger.info("Frequency not specified, default to monthly")
    if 'model' not in definitions:
        definitions['model'] = 'EC-EARTH4'
        logger.debug("Model not specified, default to EC-EARTH4")
    if 'exp' not in definitions:
        raise ValueError("Experiment name 'exp' is mandatory. This is the 4 character experiment name")
    if 'exp_name' not in definitions:
        definitions['exp_name'] = definitions['exp']
    if 'ifs_grid' not in definitions or 'nemo_grid' not in definitions:
        raise ValueError("IFS and NEMO grids are mandatory")
    if 'amip' not in definitions:
        definitions['amip'] = False
    if 'path' not in definitions:
        raise ValueError("You must provide the path where data are stored")

    # Destine fixes are True by default
    # if 'destine' not in definitions:
    #    definitions['destine'] = 'True'

    # Build the description if not provided
    if 'description' not in definitions:
        definitions['description'] = f'{definitions["model"]} {definitions["ifs_grid"]}/{definitions["nemo_grid"]} {definitions["exp_name"]} run' # noqa

    # Build the string for the frequency
    if definitions['freq'] == 'monthly':
        definitions['exp_freq'] = '1m'
    elif definitions['freq'] == 'yearly':
        definitions['exp_freq'] = '1y'
    else:
        raise ValueError("Frequency must be either 'monthly' or 'yearly'")

    # Build the fixer names
    #if definitions['destine'] == 'True':
    definitions['ifs_fixer'] = "ec-earth4-ifs"
    definitions['ice_fixer'] = "ec-earth4-nemo-ice"
    definitions['nemo_fixer'] = "ec-earth4-nemo"
    #else:
        # do something else

    # jinja2 loading and replacing (to be checked)
    templateLoader = jinja2.FileSystemLoader(searchpath='./')
    templateEnv = jinja2.Environment(loader=templateLoader, trim_blocks=True, lstrip_blocks=True)

    template = templateEnv.get_template(jinja_file)
    outputText = template.render(definitions)

    # Create output file in model folder
    configurer = ConfigPath()
    config_dir = configurer.get_config_dir()

    output_dir = os.path.join(config_dir, 'catalogs', definitions['catalog'], 'catalog', definitions['model'])
    output_filename = f"{definitions['exp_name']}.yaml"
    output_path = os.path.join(output_dir, output_filename)
    logger.debug("Output file: %s", output_path)

    if os.path.exists(output_path):
        logger.warning("File %s already exists, it will be overwritten", output_path)
        os.remove(output_path)

    with open(output_path, "w", encoding='utf8') as output_file:
        output_file.write(outputText)

    logger.info("File %s has been created in %s", output_filename, output_dir)

    # Update main.yaml model file
    main_yaml_path = os.path.join(output_dir, 'main.yaml')
    logger.debug("Main file: %s", main_yaml_path)

    main_yaml = load_yaml(main_yaml_path)
    main_yaml['sources'][definitions['exp_name']] = {
        'description': definitions['description'],
        'driver': 'yaml_file_cat',
        'args': {
            'path': f"{{{{CATALOG_DIR}}}}/{definitions['exp_name']}.yaml"
        }
    }

    dump_yaml(main_yaml_path, main_yaml)

    logger.info("%s entry in 'main.yaml' has been updated in %s", definitions['exp_name'], output_dir)

    # Check if the file is in the catalog
    sources = inspect_catalog(catalog_name=definitions['catalog'], model=definitions['model'],
                              exp=definitions['exp_name'], verbose=False)

    if sources is False:
        raise ValueError(f"Catalog {definitions['catalog']}, model {definitions['model']} and exp {definitions['exp_name']} not found in the catalog") # noqa
    else:
        logger.debug("Sources available in catalog for catalog %s model %s and exp %s: %s",
                     definitions['catalog'], definitions['model'], definitions['exp_name'], sources)

    for source in sources:
        if source != "lra-r100-monthly":
            reader = Reader(catalog=definitions['catalog'], model=definitions['model'],
                            exp=definitions['exp_name'], source=source,
                            areas=False, loglevel=loglevel)

    logger.info("Catalog generation completed")
