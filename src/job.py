import datetime
import os
from threading import Timer

from src import screenshot, config


def print_hello():
    print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    t = Timer(2, print_hello)
    t.start()


def grab_screen():
    if config.conf.cron_start != "yes":
        return
    now = datetime.datetime.now()
    d_i_r = "{0}\\{1}".format(config.conf.cron_screenshot_file_path, now.strftime('%Y-%m-%d'))
    if not os.path.exists(d_i_r):
        os.mkdir(d_i_r)

    jpg__format = "{0}\\{1}.jpg".format(d_i_r, now.strftime('%H-%M-%S'))
    # print(jpg__format)
    screenshot.window_capture(jpg__format)
    t = Timer(config.conf.cron_screenshot_time, grab_screen)
    t.start()


if __name__ == "__main__":
    config.conf.handler_config()
    # grab_screen()
