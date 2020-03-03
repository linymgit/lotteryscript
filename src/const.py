import os

SCREENSHOT_PATH = "\\temp\\screenshot.jpg"
CRON_SHOT_PATH = "\\cron_shot"
TEMP = "\\temp"
DATA_SAVE_DIR = "\\data"

OK_MP3 = "resources/ok.mp3"
FAIL_MP3 = "resources/fail.mp3"
START_MP3 = "resources/forrily.mp3"

BLUE_CIRCLE_PATH = "resources/blue.jpg"
RED_CIRCLE_PATH = "resources/red.jpg"
HE_RED_CIRCLE_PATH = "resources/_red.jpg"
HE_BLUE_CIRCLE_PATH = "resources/_blue.jpg"
ORIGIN_PATH = "resources/origin.jpg"
CLOSE_PATH = "resources/close.jpg"
GAME_START_PATH = "resources/game_start.jpg"

RED_VALUE = 1
HE_RED_V = 2
BLUE_VALUE = 3
HE_BLUE_V = 4


class Const:
    screen_path = os.getcwd() + SCREENSHOT_PATH
    cron_shot_path = os.getcwd() + CRON_SHOT_PATH
    data_save_dir = os.getcwd() + DATA_SAVE_DIR
    temp = os.getcwd() + TEMP


if __name__ == "__main__":
    print(Const.screen_path)
