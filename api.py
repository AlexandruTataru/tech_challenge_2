"""Actual API from the Tech Challenge"""
# Could have used pandas package which is more data processing orientated as far as I know
import csv
import os
import random
import functools
import datetime

REQUIRED_DATA_SET_SIZE = 10

def data_points_extractor(filepath):
    """Extractor"""

    if not os.path.exists(filepath):
        raise Exception('Ticker file does not exist')

    if not os.access(filepath, os.R_OK):
        raise Exception('Ticker file cannot be read')

    data_points = []
    with open(filepath, mode='r') as file:
        csvfile = csv.reader(file)
        for entry in csvfile:
            data_points.append([entry[0], entry[1], float(entry[2])])
        if len(data_points) < REQUIRED_DATA_SET_SIZE:
            raise Exception("Ticker file has less than 10 entries")

    start_point = random.randint(0, len(data_points) - REQUIRED_DATA_SET_SIZE)
    return data_points[start_point:start_point + REQUIRED_DATA_SET_SIZE]

def predict_next(initial_series):
    """Predict"""
    if initial_series is None or len(initial_series) < REQUIRED_DATA_SET_SIZE:
        raise Exception('Dataset must contain at least 10 entries')
    ticker = initial_series[0][0]
    date_ftm = '%d-%m-%Y'
    latest_date = datetime.datetime.strptime(initial_series[-1][1], date_ftm)
    initial_series.append([ticker,
                           (latest_date + datetime.timedelta(days=1)).strftime(date_ftm),
                           sorted(initial_series, key=functools.cmp_to_key(lambda l, r: r[2] - l[2]))[1][2]
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