Pre-Interview Coding Challenge
-------------
Challenge 2: Backend – Predict next 3 values of Stock price (timeseries data)

Usage
-------------

```python
$ python3 predictor.py --help
usage: predictor.py [-h] [-n NR_FILES] [-p] [-i INPUT_FOLDER] [-o OUTPUT_FOLDER]

Predict next 3 values of Stock price (timeseries data)

options:
  -h, --help            show this help message and exit
  -n NR_FILES, --nr_files NR_FILES
                        number of files to be sampled for each Stock Exchange
  -p, --parallel        parse each Stock Exchange on a separate thread
  -i INPUT_FOLDER, --input_folder INPUT_FOLDER
                        folder containing multiple Stock Exchange folders with again multiple CSV files
  -o OUTPUT_FOLDER, --output_folder OUTPUT_FOLDER
                        folder used to dump parsed output, similar in structure to input folder

Created by Alexandru-Flavian Tataru for the LSEG Pre-Interview Code Challenge
```

Quick start
-----------
Below prompt is an example of best usage
```python
$ python3.10 predictor.py -n 2 -i /Users/atataru/Desktop/tasklsegresurse/input/ -o /Users/atataru/Desktop/tasklsegresurse/output -p
```

Please be aware that:
* Input/output folders location defaults to '.' (current folder)
* Input/output folders can be given as absolute/relative/expandable paths
* Default value for number of input files is 2

Developer mentions
-----------
* The actual required two methods API from the assignment is isolated in `api.py` making it more portable
* A logging system is used in the main usage script except in the actual API which uses exceptions
* The code was developed while in parallel running code analysis tools (pylint, flink8)
* A form of unit testing is also started as part of the project
* A Makefile is available to more easily run things locally. I often found myself running `make lint` and `make style`
* The project uses GitHub actions which run after each push

Example outputs
-----------
In below output we can see the integrated logger with a custom pattern.
```python
$ python3.10 predictor.py -n 2 -i /Users/atataru/Desktop/tasklsegresurse/input/ -o /Users/atataru/Desktop/tasklsegresurse/output
2024-12-11 02:19:00,345 - __main__ - 8540193344 -    INFO - Starter the app with below arguments
2024-12-11 02:19:00,346 - __main__ - 8540193344 -    INFO - Namespace(nr_files=2, parallel=False, input_folder='/Users/atataru/Desktop/tasklsegresurse/input/', output_folder='/Users/atataru/Desktop/tasklsegresurse/output')
2024-12-11 02:19:00,346 - __main__ - 8540193344 -   DEBUG - Input folder absolute path is: /Users/atataru/Desktop/tasklsegresurse/input
2024-12-11 02:19:00,346 - __main__ - 8540193344 -   DEBUG - Output folder absolute path is: /Users/atataru/Desktop/tasklsegresurse/output
2024-12-11 02:19:00,346 - __main__ - 8540193344 -    INFO - /Users/atataru/Desktop/tasklsegresurse/input/NASDAQ
2024-12-11 02:19:00,346 - __main__ - 8540193344 -    INFO - Stock exchange name: NASDAQ
2024-12-11 02:19:00,346 - __main__ - 8540193344 -    INFO - Ticker file: TSLA.csv
2024-12-11 02:19:00,346 - __main__ - 8540193344 -    INFO - Input folder: /Users/atataru/Desktop/tasklsegresurse/input
2024-12-11 02:19:00,346 - __main__ - 8540193344 -    INFO - Output folder: /Users/atataru/Desktop/tasklsegresurse/output
2024-12-11 02:19:00,348 - __main__ - 8540193344 -    INFO - Stock exchange name: NASDAQ
2024-12-11 02:19:00,348 - __main__ - 8540193344 -    INFO - Ticker file: FLTR.csv
2024-12-11 02:19:00,348 - __main__ - 8540193344 -    INFO - Input folder: /Users/atataru/Desktop/tasklsegresurse/input
2024-12-11 02:19:00,348 - __main__ - 8540193344 -    INFO - Output folder: /Users/atataru/Desktop/tasklsegresurse/output
```
In below output we can see that we run in threaded mode and each stock exchange is printing the log output with a different thread id.
```python
$ python3.10 predictor.py -n 2 -i /Users/atataru/Desktop/tasklsegresurse/input/ -o /Users/atataru/Desktop/tasklsegresurse/output -p
2024-12-11 02:19:26,247 - __main__ - 8540193344 -    INFO - Starter the app with below arguments
2024-12-11 02:19:26,247 - __main__ - 8540193344 -    INFO - Namespace(nr_files=2, parallel=True, input_folder='/Users/atataru/Desktop/tasklsegresurse/input/', output_folder='/Users/atataru/Desktop/tasklsegresurse/output')
2024-12-11 02:19:26,247 - __main__ - 8540193344 -   DEBUG - Input folder absolute path is: /Users/atataru/Desktop/tasklsegresurse/input
2024-12-11 02:19:26,247 - __main__ - 8540193344 -   DEBUG - Output folder absolute path is: /Users/atataru/Desktop/tasklsegresurse/output
2024-12-11 02:19:26,247 - __main__ - 8540193344 -    INFO - /Users/atataru/Desktop/tasklsegresurse/input/NASDAQ
2024-12-11 02:19:26,248 - __main__ - 8540193344 -    INFO - Script is running in threaded mode, one for each exchange
2024-12-11 02:19:26,248 - __main__ - 6151499776 -    INFO - Stock exchange name: NASDAQ
2024-12-11 02:19:26,248 - __main__ - 6151499776 -    INFO - Ticker file: TSLA.csv
2024-12-11 02:19:26,248 - __main__ - 6151499776 -    INFO - Input folder: /Users/atataru/Desktop/tasklsegresurse/input
2024-12-11 02:19:26,248 - __main__ - 6151499776 -    INFO - Output folder: /Users/atataru/Desktop/tasklsegresurse/output
2024-12-11 02:19:26,248 - __main__ - 6168326144 -    INFO - Stock exchange name: NASDAQ
2024-12-11 02:19:26,248 - __main__ - 6168326144 -    INFO - Ticker file: FLTR.csv
2024-12-11 02:19:26,248 - __main__ - 6168326144 -    INFO - Input folder: /Users/atataru/Desktop/tasklsegresurse/input
2024-12-11 02:19:26,248 - __main__ - 6168326144 -    INFO - Output folder: /Users/atataru/Desktop/tasklsegresurse/output
```