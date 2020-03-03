import threading
import time

from src import config, const, pos, job
from playsound import playsound


def check_circle():
    print("开始识别...")
    c = threading.Thread(target=pos.check_circle, args=(const.RED_CIRCLE_PATH, config.conf.red_circle_threshold))
    c.start()
    while c.is_alive():
        time.sleep(1)
    else:
        c = threading.Thread(target=pos.check_circle,
                             args=(const.HE_RED_CIRCLE_PATH, config.conf.he_red_circle_threshold))
        c.start()
        while c.is_alive():
            time.sleep(1)
        else:
            c = threading.Thread(target=pos.check_circle,
                                 args=(const.BLUE_CIRCLE_PATH, config.conf.blue_circle_threshold))
            c.start()
            while c.is_alive():
                time.sleep(1)
            else:
                c = threading.Thread(target=pos.check_circle,
                                     args=(const.HE_BLUE_CIRCLE_PATH, config.conf.he_red_circle_threshold))
                c.start()
                while c.is_alive():
                    time.sleep(1)
                else:
                    c = threading.Thread(target=pos.pick_origin, args=(True,))
                    c.start()
                    while c.is_alive():
                        time.sleep(1)
    check_result = input("识别是否成功(yes是成功no是失败)？")
    if check_result == "yes":
        return True
    return False


def playStartMp3():
    playsound(config.conf.start_mp3)


if __name__ == "__main__":
    print("分析程序启动...")
    config.conf.handler_config()
    print("程序成功启动...")
    playStartMp3()
    print("关注我们：    http://www.forrily.com")
    recognition = True  # 识别校验状态

    print("开启截屏定时任务,{0}秒抓取一次屏幕".format(config.conf.cron_screenshot_time))
    job.grab_screen()

    if config.conf.check_threshold == "yes":  # 检查图片识别是否正确
        recognition = check_circle()

    if recognition:
        c = threading.Thread(target=pos.fill_pos_array, args=())
        c.start()

        d = threading.Thread(target=pos.handler_web_close, args=())
        d.start()

        e = threading.Thread(target=pos.handler_new_game(), args=())
        e.start()

else:
    print("修改参数，识别检测成功之后重试!!!")
