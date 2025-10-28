#!/usr/bin/env python3

import argparse
import sys
from aqua.logger import log_configure
from aqua.util import load_yaml, get_arg
from gribber import Gribber


def parse_arguments(args):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Gribber CLI")

    parser.add_argument("-l", "--loglevel", type=str, default="WARNING",
                        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    parser.add_argument("--config", type=str, default="config.yaml",
                        help="Path to the configuration file")

    return parser.parse_args(args)


if __name__ == "__main__":

    args = parse_arguments(sys.argv[1:])
    loglevel = get_arg(args, "loglevel", "WARNING")
    logger = log_configure(log_level=loglevel, log_name="CLI Gribber")
    logger.info("Starting Gribber CLI")

    configfile = args.config
    config = load_yaml(configfile, loglevel)

    logger.debug(f"Config file: {config}")

    catalog = config['dataset'].get('catalog')
    model = config['dataset'].get('model')
    exp = config['dataset'].get('exp')
    source = config['dataset'].get('source')

    nprocs = config.get('nprocs', 1)
    dirdict = config.get('dirdict', {'datadir': None, 'tmpdir': None,
                         'jsondir': None, 'configdir': None})
    description = config.get('description', None)

    grib = Gribber(catalog=catalog, model=model, exp=exp,
                   source=source, nprocs=nprocs, dirdict=dirdict,
                   description=description, loglevel=loglevel)
