"""Main script"""
import argparse
import logging
import os
import sys

import constants
import api

logger = logging.getLogger(__name__)


def logger_setup():
    """This function initializes the logger"""
    log_format = '%(asctime)s - %(name)s - %(levelname)7s - %(message)s'
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
    logger.debug("Input folder absolute path is: %s", input_folder)
    args.input_folder = input_folder
    output_folder = os.path.abspath(args.output_folder)
    logger.debug("Output folder absolute path is: %s", output_folder)
    args.output_folder = output_folder


def __validate_folder(folder, requirements):
    """This function should not be used.
    Kept it just as an example of what I would have liked to do.
    We could have given a different set of validation
    (ex: input folder only needs read permissions while
    output folder needs write permissions)
    and we could check that entire set of requirements
    Example call would have been
    __validate_folder(stock_exchange_input_folder,
                          {os.path.exists, os.path.isdir, lambda dir: os.access(dir, os.R_OK)})
    """
    isValidFolder = True
    for requirement in requirements:
        validation_res = requirement(folder)
        isValidFolder = isValidFolder and validation_res
        logger.debug("Requirement %s returned %s",
                     requirement, bool(validation_res))
    logger.info("Validated folder: %s as %s", folder, isValidFolder)
    return isValidFolder


def process_stock_exchange(stock_exchange_name, input_folder, output_folder):
    """This is the main processing function"""
    pass


def main():
    """Main method"""
    logger_setup()
    args = handle_args()
    normalize_input(args)

    # List all sub-folders in a folder
    for folder in next(os.walk(args.input_folder))[1]:
        logger.info(os.path.join(args.input_folder, folder))
        stock_exchange_input_folder = os.path.join(args.input_folder, folder)
        stock_exchange_output_folder = os.path.join(args.output_folder, folder)
        process_stock_exchange(folder,
                               stock_exchange_input_folder,
                               stock_exchange_output_folder)


if __name__ == '__main__':
    # main()
    data = api.data_points_extractor('/Users/atataru/Desktop/tasklsegresurse/stock_price_data_files/NASDAQ/TSLA.csv')
    print(data)
    data = api.predict_next(data)
    print(data)