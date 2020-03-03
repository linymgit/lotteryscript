import datetime
import logging


# # 创建一个logging对象
# logger = logging.getLogger()
# # 创建一个文件对象  创建一个文件对象,以UTF-8 的形式写入 标配版.log 文件中
# fh = logging.FileHandler('temp/sys.log', encoding='utf-8')
# # 创建一个屏幕对象
# sh = logging.StreamHandler()
# # 配置显示格式  可以设置两个配置格式  分别绑定到文件和屏幕上
# formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
# fh.setFormatter(formatter)  # 将格式绑定到两个对象上
# sh.setFormatter(formatter)
#
# logger.addHandler(fh)  # 将两个句柄绑定到logger
# logger.addHandler(sh)
#
# logger.setLevel(10)  # 总开关
# fh.setLevel(10)  # 写入文件的从10开始
# sh.setLevel(30)  # 在屏幕显示的从30开始
#
# logging.debug('debug message')
# logging.info('info message')
# logging.warning('warning message')
# logging.error('error message')
# logging.critical('critical message')

class B:
    def __init__(self):
        self.success_logger = logging.getLogger()
        self.success_logger.setLevel(logging.DEBUG)  # 总开关
        success_formatter = logging.Formatter('%(asctime)s %(message)s')
        success_logger_handler = logging.FileHandler(
            "{0}{1}成功记录.{2}".format('data/', datetime.datetime.now().strftime("%Y-%m-%d"), 'log'),
            encoding='utf-8')
        success_logger_handler.setFormatter(success_formatter)
        self.success_logger.addHandler(success_logger_handler)

    def log(self):
        self.success_logger.debug("hello world BBB")


class A:
    def __init__(self):
        self.sys_logger = logging.getLogger()
        self.sys_logger.setLevel(logging.INFO)  # 总开关
        sys_formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        sys_logger_handler = logging.FileHandler(
            "{0}{1}sys.{2}".format('log/', datetime.datetime.now().strftime("%Y-%m-%d"), 'log'),
            encoding='utf-8')
        sys_logger_handler.setFormatter(sys_formatter)
        self.sys_logger.addHandler(sys_logger_handler)

    def log(self):
        self.sys_logger.info("hello world")
