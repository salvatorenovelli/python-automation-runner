import atexit
import logging
import os
import sys
import time
from multiprocessing import freeze_support

from system_hotkey import SystemHotkey, SystemRegisterError

from external_script_runner import ExternalScript

logging.basicConfig(format='[%(asctime)-15s] [%(process)-5d] %(levelname)-5s [%(filename)-30s] %(message)s',
                    level=logging.INFO)

external_script = None
run = True


def init_external_script():
    global external_script
    external_script = ExternalScript("external script", sys.argv[1])


def handle_m(msg):
    global external_script
    logging.info("CTRL+ALT+M pressed, starting %s", sys.argv[1])
    external_script.start_main_loop()


def handle_j(msg):
    global external_script
    logging.info("CTRL+ALT+J pressed, stopping script")
    external_script.stop_main_loop()


def handle_q(msg):
    global run
    logging.info("CTRL+ALT+Q pressed, terminating script")
    run = False
    sys.exit(0)


def uncaught_exception_handler(exctype, value, tb):
    if isinstance(value, SystemRegisterError):
        logging.error("Unable to register hotkey %s", str(value))
    else:
        logging.error(str(value))


def register_hotkeys():
    sys.excepthook = uncaught_exception_handler
    hk = SystemHotkey()
    hk.register(('control', 'alt', 'm'), callback=handle_m)
    hk.register(('control', 'alt', 'j'), callback=handle_j)
    hk.register(('control', 'alt', 'q'), callback=handle_q)


def cleanup():
    external_script.stop_main_loop()


if __name__ == '__main__':

    freeze_support()

    atexit.register(cleanup)

    logger = logging.getLogger("main")

    logger.info("|*******************************************************************|")
    logger.info("|*                 Welcome to Terminal Automation!                 *|")
    logger.info("|*                 Today is a wonderful day!                       *|")
    logger.info("|*******************************************************************|")

    logger.info("Current folder is: " + os.path.dirname(os.path.abspath('__file__')))
    logger.info('Provided script: %s', sys.argv[1])

    try:

        register_hotkeys()
        init_external_script()
        logger.info("Press CTRL+ALT+Q terminate the script...")
        while run:
            time.sleep(.5)
        cleanup()

    except Exception as e:
        logging.error("Error while initialising: " + str(e))
        logging.info("Press any key to exit")
        input()
