import logging
import os
import signal
import time
from multiprocessing import Process


class ExternalScript:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.process = None

    def start_main_loop(self):
        if self.process is None:
            self.process = Process(target=run_external_script_main_loop, args=(self.name, self.path))
            self.process.start()
            logging.info("External script started. PID: %d", self.process.pid)

    def stop_main_loop(self):
        if self.process is not None:
            logging.info("Killing external script with PID: %d", self.process.pid)
            os.kill(self.process.pid, signal.SIGTERM)
            self.process = None


def run_external_script_main_loop(name, path):
    try:
        script = import_source(name, path)
        logging.info("Script loaded")
        while 1:
            start = time.time()
            try:
                script.main_loop()
            except Exception as e:
                logging.error("Error in script '%s': %s", path, str(e))
            if (time.time() - start) < .05:
                time.sleep(1)
    except Exception as e1:
        logging.error("Unable to run main_loop: " + str(e1))


def import_source(name, path):
    from importlib.machinery import SourceFileLoader
    return SourceFileLoader(name, path).load_module()
