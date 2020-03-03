import os
from configparser import ConfigParser

from src import const

filename = 'conf/configuration.ini'


class Config:
    def __init__(self):
        cp = ConfigParser()
        cp.read(filename)
        self.cp = cp
        self.root_id = self.cp.get("lottery", "root_id")
        self.screenshot_main_time = self.cp.getfloat("lottery", "screenshot_main_time")
        self.check_threshold = self.cp.get("lottery", "check_threshold")
        self.blue_circle_threshold = self.cp.getfloat("lottery", "blue_circle_threshold")
        self.he_blue_circle_threshold = self.cp.getfloat("lottery", "he_blue_circle_threshold")
        self.red_circle_threshold = self.cp.getfloat("lottery", "red_circle_threshold")
        self.he_red_circle_threshold = self.cp.getfloat("lottery", "he_red_circle_threshold")
        self.data_save_dir = self.cp.get("lottery", "data_save_dir")
        self.ok_times_remind = self.cp.getfloat("lottery", "ok_times_remind")
        self.ok_mp3 = self.cp.get("lottery", "ok_mp3")
        self.fail_times_remind = self.cp.getfloat("lottery", "fail_times_remind")
        self.fail_mp3 = self.cp.get("lottery", "fail_mp3")
        self.start_mp3 = self.cp.get("lottery", "start_mp3")
        self.blank_len = self.cp.getfloat("lottery", "blank_len")
        self.cron_screenshot_time = self.cp.getfloat("cron", "cron_screenshot_time")
        self.cron_screenshot_file_path = self.cp.get("cron", "cron_screenshot_file_path")
        self.cron_start = self.cp.get("cron", "start")
        self.logger_level = self.cp.getint("logger", "level")
        # self.pos_time = self.cp.getfloat("pos", "pos_time")
        # self.pos_threshold = self.cp.getfloat("pos", "pos_threshold")

    def get_screen_shot_main_time(self):
        """
        抓取主屏幕时间间隔
        :return:
        """
        return self.screenshot_main_time

    def __init_file(self, path, ini_path, name):
        if path == "":
            path = ini_path
            print("***无自定义" + name + "的存储路径，默认路径是:" + ini_path)
        else:
            print("***" + name + "的存储路径，路径是:" + path)
        if not os.path.exists(path):
            print("***创建了" + name + "的存储目录：" + path)
            os.makedirs(path)
        return path

    def handler_config(self):
        """
        创建文件存储目录
        :return:
        """
        print("**初始化配置文件(conf/configuration.ini)...")

        self.cron_screenshot_file_path = self.__init_file(self.cron_screenshot_file_path, const.Const.cron_shot_path,
                                                          "定时截图")
        self.data_save_dir = self.__init_file(self.data_save_dir, const.Const.data_save_dir, "统计数据")

        self.ok_mp3 = self.__init_file(self.ok_mp3, const.OK_MP3, "成功提醒音乐")

        self.fail_mp3 = self.__init_file(self.fail_mp3, const.FAIL_MP3, "失败提醒音乐")

        self.start_mp3 = self.__init_file(self.start_mp3, const.START_MP3, "程序启动提醒音乐")

        if os.path.exists(const.Const.screen_path):
            os.remove(const.Const.screen_path)
        if os.path.exists(self.data_save_dir + '//ing.json'):
            os.remove(self.data_save_dir + '//ing.json')
        if os.path.exists(self.data_save_dir + '//array_ing.json'):
            os.remove(self.data_save_dir + '//array_ing.json')


conf = Config()

if __name__ == "__main__":
    config = Config()
    print(config.screenshot_main_time)
