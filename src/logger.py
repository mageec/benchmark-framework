import multiprocessing
import os
import threading
import time

import sys
sys.path.append(os.path.dirname(__file__))

import dbi

class Logger:
# Log can be a file location or stream
    def __init__(self, log=os.path.abspath("./log.txt"), db='db/development.sqlite3'):
        self.log = log
        if type(self.log) is str: # We need to delete the old file before we append to it
            try:
                os.remove(self.log)
            except FileNotFoundError:
                pass # We don't care if the file doesn't already exist
        self.dbi = dbi.DBi(os.path.abspath(db))

    def log_info(self, sender, msg):
        self.__log_message("INFO", sender, msg)

    def log_warn(self, sender, msg):
        self.__log_message("WARN", sender, msg)

    def log_erro(self, sender, msg):
        self.__log_message("ERRO", sender, msg)

    def add_run(self, *args):
        return self.dbi.add_run(*args)

    def record_results(self, results):
        #self.log_info("logger", "Adding the following results to the database:")
        #self.log_info("logger", str(results))
        self.log_info("logger", "Adding results to the database")
        if results is None:
            self.log_erro("logger", "Got no results.")
            self.log_erro("logger", "Something probably went wrong with the test.")
        else:
            self.dbi.record(results.run.id, results.results)
            self.log_info("logger", "Finished adding results")

    def __log_message(self, level, sender, msg):
        str_time = time.strftime("%Y-%m-%d %H:%M:%S")
        with self:
            self.stream.write("[{}] {}: {}: {}\n".format(str_time, level.upper(), sender, msg))

    def __enter__(self):
        if type(self.log) is str:
            self.stream = open(self.log, 'a')
        else:
            self.stream = self.log
        self.dbi.__enter__()
        return self

    def __exit__(self, err_type, value, traceback):
        self.dbi.__exit__(err_type, value, traceback)
        if type(self.log) is str:
            self.stream.close()
