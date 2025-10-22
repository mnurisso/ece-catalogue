#!/usr/bin/env python3
"""
Command-line interface for a Custom diagnostic.
"""
import argparse
import sys

from aqua.logger import log_configure
from aqua.util import get_arg
from aqua.diagnostics.core import template_parse_arguments, open_cluster, close_cluster
from aqua import Reader


def parse_arguments(args):
    """Parse command-line arguments for Custom diagnostic.

    Args:
        args (list): list of command-line arguments to parse.
    """
    # The default parser arguments are described here: https://aqua.readthedocs.io/en/latest/stateoftheart_diagnostics/index.html#diagnostics-cli-arguments
    # Additional arguments specific to this script can be added here.
    parser = argparse.ArgumentParser(description='Template CLI')
    parser = template_parse_arguments(parser)

    # Example of adding custom arguments
    # parser.add_argument('--source_oce', type=str,
    #                     help='source of the oceanic data, to be used when oceanic data is in a different source than atmospheric data',
    #                     default=None)
    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])

    loglevel = get_arg(args, 'loglevel', 'WARNING')
    logger = log_configure(log_level=loglevel, log_name='Custom CLI')

    # This will open a Dask cluster if requested, -n is used to set the number of workers
    cluster = get_arg(args, 'cluster', None)
    nworkers = get_arg(args, 'nworkers', None)

    client, cluster, private_cluster, = open_cluster(nworkers=nworkers, cluster=cluster, loglevel=loglevel)

    # The basic requirements to run a diagnostic is to access data with the Reader class
    # Here we get from the command line the necessary arguments to initialize it.
    catalog = get_arg(args, 'catalog', None)
    model = get_arg(args, 'model', None)
    exp = get_arg(args, 'exp', None)
    source = get_arg(args, 'source', None)
    realization = get_arg(args, 'realization', None)
    # This reader_kwargs will be used if the dataset corresponding value is None or not present
    if realization:
        reader_kwargs = {'realization': realization}
    else:
        reader_kwargs = config_dict['datasets'][0].get('reader_kwargs') or {}

    # We open the Reader. Here we are not opening any observational dataset, but it is possible to do so
    # with another Reader instance.
    reader = Reader(catalog=catalog, model=model, exp=exp, source=source,
                    reader_kwargs=reader_kwargs, loglevel=loglevel)
    # startdate, enddate and variables list (as var argument) can be also passed to the Reader
    # depending on the use case.
    data = reader.retrieve()

    # Custom diagnostic:
    # data is now an xarray.Dataset with the data for the specified model/exp/source
    # Here you can implement the desired diagnostic analysis.

    # At the end of the analysis, close the cluster if opened
    close_cluster(client=client, cluster=cluster, private_cluster=private_cluster, loglevel=loglevel)

    logger.info("Custom diagnostic completed.")
