"""
predictor.py
"""
import argparse
import logging
import os
import sys
import csv
import threading

import constants
import api

logger = logging.getLogger(__name__)
mutex = threading.Lock()


def logger_setup():
    """Configure the logger"""
    log_format = '%(asctime)s - %(name)s - %(thread)d - %(levelname)7s - %(message)s'
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
    """Take script arguments and normalize them for processing"""
    input_folder = os.path.abspath(args.input_folder)
    logger.debug("Input folder absolute path is: %s", input_folder)
    args.input_folder = input_folder

    if not os.path.exists(args.input_folder):
        logger.error("Input folder does not exist")
        sys.exit(constants.EXIT_CODE_INVALID_INPUT_FOLDER)

    output_folder = os.path.abspath(args.output_folder)
    logger.debug("Output folder absolute path is: %s", output_folder)
    args.output_folder = output_folder


def __validate_folder(folder, requirements):
    """This function should not be used.
    Kept it just as an example of what I would have liked to do.
    We could have given a different set of requirements
    (ex: input folder only needs read permissions while
    output folder needs write permissions)
    and we could check that entire set of requirements
    Example call would have been
    isValidFolder = __validate_folder(stock_exchange_input_folder,
                          {os.path.exists, os.path.isdir, lambda dir: os.access(dir, os.R_OK)})
    """
    is_valid_folder = True
    for requirement in requirements:
        validation_res = requirement(folder)
        is_valid_folder = is_valid_folder and validation_res
        logger.debug("Requirement %s returned %s",
                     requirement, bool(validation_res))
    logger.info("Validated folder: %s as %s", folder, is_valid_folder)
    return is_valid_folder


def process_stock_exchange(stock_exchange_name, ticker_file, input_folder, output_folder):
    """Main processing method. Encapsulates all logic to read
    one ticker CSV files, predict extra values and write them to output folder"""
    logger.info("Stock exchange name: %s", stock_exchange_name)
    logger.info("Ticker file: %s", ticker_file)
    logger.info("Input folder: %s", input_folder)
    logger.info("Output folder: %s", output_folder)
    try:
        dataset = api.data_points_extractor(os.path.join(input_folder,
                                                         stock_exchange_name,
                                                         ticker_file))
        new_dataset = api.predict_next(dataset)

        """When in multithreaded mode I could try to create the same folder
        from multiple threads. I could have used exception handling but also
        wanted to show the mutex guarding approach which is applied only on this
        section of code to reduce impact as all the other code segments are independent
        """
        with mutex:
            if not os.path.exists(os.path.join(output_folder, stock_exchange_name)):
                os.makedirs(os.path.join(output_folder, stock_exchange_name))

        with open(os.path.join(output_folder, stock_exchange_name, ticker_file),
                  'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(new_dataset)
    except api.APIException as error:
        logger.error("API Exception while processing ticker file %s: %s", ticker_file, error)
    except Exception as error:
        logger.error("General Exception while processing ticker file %s: %s", ticker_file, error)


def main():
    """Main method"""
    logger_setup()
    args = handle_args()
    normalize_input(args)

    threads = []
    for folder in next(os.walk(args.input_folder))[1]:
        logger.info(os.path.join(args.input_folder, folder))
        stock_exchange_input_folder = str(os.path.join(args.input_folder, folder))
        left_files_to_parse = args.nr_files
        for entry in os.listdir(stock_exchange_input_folder):
            if os.path.isfile(os.path.join(stock_exchange_input_folder, entry)) and entry.endswith(".csv"):
                if left_files_to_parse == 0:
                    break
                left_files_to_parse = left_files_to_parse - 1
                if args.parallel:
                    threads.append(threading.Thread(target=process_stock_exchange,
                                                    args=(folder,entry, args.input_folder, args.output_folder)))
                else:
                    process_stock_exchange(folder, entry,
                               args.input_folder,
                               args.output_folder)
    if args.parallel and len(threads) > 0:
        logger.info('Script is running in threaded mode, one for each exchange')
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


if __name__ == '__main__':
    main()
