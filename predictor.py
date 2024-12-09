"""Main script"""
import argparse
import logging
import os
import sys

import constants

logger = None


def logger_setup():
    """This function initializes the logger"""
    log_format = '%(asctime)s - %(name)s - %(levelname)7s - %(message)s'
    global logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format=log_format)


def handle_args():
    """Parse script parameters and apply functional logic"""
    parser = argparse.ArgumentParser(
        prog='predictor.py',
        description='Predict next 3 values of Stock price (timeseries data)',
        epilog='Created by Alexandru-Flavian Tataru '
               'for the LSEG Pre-Interview Code Challenge')

    parser.add_argument('-n', '--nr_files', type=int,
                        help='number of files to be sampled '
                             'for each Stock Exchange', default=2)
    parser.add_argument('-p', '--parallel',
                        help='parse each Stock Exchange '
                             'on a separate thread',
                        action='store_true', default=False)
    parser.add_argument('-i', '--input_folder', type=str,
                        help='folder containing multiple Stock Exchange '
                             'folders with again multiple CSV files',
                        default='.')
    parser.add_argument('-o', '--output_folder', type=str,
                        help='folder used to dump parsed output, '
                             'similar in structure to input folder',
                        default='.')

    args = parser.parse_args()
    logger.info('Starter the app with below arguments')
    logger.info(args)

    if args.nr_files > 2:
        logger.error("Cannot specify more than 2 files per exchange")
        sys.exit(constants.EXIT_CODE_WRONG_NR_FILES)

    return args


def normalize_input(args):
    """This function take the arguments and prepares them for processing"""
    input_folder = os.path.abspath(args.input_folder)
    logger.debug(input_folder)
    output_folder = os.path.abspath(args.output_folder)
    logger.debug(output_folder)


def main():
    """Main method"""
    logger_setup()
    args = handle_args()
    normalize_input(args)


if __name__ == '__main__':
    main()
