"""
api.py
"""
# Could have used pandas package for processing
# the CSV file which is more suitable
import csv
import os
import random
import functools
import datetime

REQUIRED_DATA_SET_SIZE = 10


class APIException(Exception):
    """Non-generic exception created for the API"""
    pass


def data_points_extractor(filepath):
    """Read input CSV file and return 10 consecutive entries
    starting from a random position"""

    if not os.path.exists(filepath):
        raise APIException('Ticker file does not exist')

    if not os.access(filepath, os.R_OK):
        raise APIException('Ticker file cannot be read')

    data_points = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        csvfile = csv.reader(file)
        for entry in csvfile:
            data_points.append([entry[0], entry[1], float(entry[2])])
        if len(data_points) < REQUIRED_DATA_SET_SIZE:
            raise APIException("Ticker file has less than 10 entries")

    start_point = random.randint(0, len(data_points) - REQUIRED_DATA_SET_SIZE)
    return data_points[start_point:start_point + REQUIRED_DATA_SET_SIZE]


def predict_next(initial_series):
    """Based on an initial set of 10 entries will return a
    13 entries list with last 3 being predicted"""
    if initial_series is None or len(initial_series) < REQUIRED_DATA_SET_SIZE:
        raise APIException('Dataset must contain at least 10 entries')
    ticker = initial_series[0][0]
    date_ftm = '%d-%m-%Y'
    latest_date = datetime.datetime.strptime(initial_series[-1][1], date_ftm)
    initial_series.append([ticker,
                           (latest_date + datetime.timedelta(days=1)).strftime(date_ftm),
                           sorted(initial_series,
                                  key=functools.cmp_to_key(lambda left, right: right[2] - left[2]))[1][2]
                           ])
    initial_series.append([ticker,
                           (latest_date + datetime.timedelta(days=2)).strftime(date_ftm),
                           (initial_series[-2][2] + initial_series[-1][2]) * 0.5
                           ])
    initial_series.append([ticker,
                           (latest_date + datetime.timedelta(days=3)).strftime(date_ftm),
                           (initial_series[-2][2] + initial_series[-1][2]) * 0.5
                           ])
    return initial_series
