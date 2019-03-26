from datetime import datetime

class Logger(object):
    """
        Standard output logger. It is designed to display debug messages, if the
        verbosity level allows it, and critical messages no matter what.
    """

    def __init__(self, verbose=True, name="api"):
        self.verbose = verbose
        self.name = name
        self.output_file = "logs/app_logs.txt"
        self.request_data_output = "logs/request_data.txt"

    def info(self, message):
        out_to_file = open(self.output_file, 'a')
        if self.verbose:
            log = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " " + self.name +" : " + message
            print(log)
            out_to_file.write(log + "\n")
        out_to_file.close()

    def critical(self, message):
        out_to_file = open(self.output_file, 'a')
        log = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " " + self.name +" : " + message
        print(log)
        out_to_file.write(log + "\n")

    def request_data(self, timeseries):
        out_to_file = open(self.request_data_output, 'a')
        if self.verbose:
            log = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " " + self.name + " : " + timeseries
            out_to_file.write(log + "\n")
        out_to_file.close()