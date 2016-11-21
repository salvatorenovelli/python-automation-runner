import logging
import time

import user_interaction as ui

logging.info("External script loaded")


def main_loop():
    logging.info("Current cursor position is: %s", str(ui.get_cursor_pos()))
    logging.info("Current foreground application executable is: %s", str(ui.get_cur_window_executable()))

    logging.info("Clicking...")
    ui.click(100, 100)
    time.sleep(10)
