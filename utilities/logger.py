import logging
import os
import time

def build_logger():
    """
    Instantiate a logger based on the verbosity specified in gfw-sync.py at the commandline
    logging example: https://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
    :param verbosity:
    :return: a logger object used by the rest of the application
    """

    # Set logging output file, verbosity, and format
    log_file = os.path.join(os.getcwd(), 'logs', time.strftime("%Y%m%d") + '.log')
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s',
                        datefmt='%H:%M:%S')

    # Set properties to that logging messages are displayed at the commandline as well
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(console)

    # these libraries log automatically; set to only show critical messages
    logging.getLogger('oauth2client').setLevel(logging.CRITICAL)
    logging.getLogger("requests").setLevel(logging.CRITICAL)

    return logging.getLogger()
