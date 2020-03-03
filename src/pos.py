import datetime
import logging
import math
import os
import shutil
import time

import aircv as ac
import win32api
import win32con
from playsound import playsound

from src import screenshot, const, config, pos_json


def print_name(circle_path):
    if circle_path == const.RED_CIRCLE_PATH:
        return "红色圆圈"
    if circle_path == const.HE_RED_CIRCLE_PATH:
        return "（和）红色圆圈"
    if circle_path == const.BLUE_CIRCLE_PATH:
        return "蓝色圆圈"
    if circle_path == const.HE_BLUE_CIRCLE_PATH:
        return "（和）蓝色圆圈"


def print_name_by_value(val):
    if val == const.RED_VALUE:
        return "红色"
    if val == const.HE_RED_V:
        return "红色1"
    if val == const.BLUE_VALUE:
        return "蓝色"
    if val == const.HE_BLUE_V:
        return "蓝色1"


def check_circle(circle_path, threshold):
    print(print_name(circle_path))
    i = 0
    while i < 60:
        i += 1
        screenshot.window_capture(const.Const.screen_path)
        try:
            mainScreen = ac.imread(const.Const.screen_path)
            circleScreen = ac.imread(circle_path)
            template = ac.find_all_template(mainScreen, circleScreen, rgb=True, threshold=threshold, bgremove=True)
            if template is None or len(template) <= 0:
                continue
            else:
                sort_template = sorted(template, key=lambda x: x["result"])
                for t in sort_template:
                    # print(t['rectangle'][1])
                    win32api.SetCursorPos((int(t['result'][0]), int(t['result'][1])))
                    # win32api.SetCursorPos((int(t['rectangle'][1][0]), int(t['rectangle'][1][1])))
                    time.sleep(0.5)
                time.sleep(1)
                break
        except:
            pass
        time.sleep(config.conf.screenshot_main_time)
    else:
        print(print_name(circle_path) + ",没有识别出来")


def pick_origin(is_check):
    i = -300
    if is_check:
        print("第一个格子的坐标（用于定位其他的格子）")
        i = 0

    while i < 60:
        i += 1
        screenshot.window_capture(const.Const.screen_path)
        mainScreen = ac.imread(const.Const.screen_path)
        originScreen = ac.imread(const.ORIGIN_PATH)
        time.sleep(config.conf.screenshot_main_time)
        template = ac.find_template(mainScreen, originScreen, threshold=0.9)
        if template is None:
            continue
        # print(template['rectangle'][1])
        if is_check:
            win32api.SetCursorPos(template['rectangle'][1])
        return template['rectangle'][1]
    return None


pos_list = list()
# pos_array = [[0 for i in range(6)] for j in range(30)]

sys_logger = logging.getLogger()
sys_logger.setLevel(config.conf.logger_level)
sys_formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
sys_logger_handler = logging.FileHandler(
    "{0}{1}sys.{2}".format('log/', datetime.datetime.now().strftime("%Y-%m-%d"), 'log'),
    encoding='utf-8')
sys_logger_handler.setFormatter(sys_formatter)
sys_logger.addHandler(sys_logger_handler)


def get_pos(xy, origin):
    x = math.fabs(xy[0] - origin[0]) / (config.conf.blank_len + 2)
    if x > 23:
        sys_logger.error("{0}{1}{2}{3};x={4}".format("x溢出", origin, xy, config.conf.blank_len, x))
        return None
    y = math.fabs(xy[1] - origin[1]) / config.conf.blank_len
    if y > 6:
        sys_logger.error("{0}{1}{2}{3};y={4}".format("y溢出", origin, xy, config.conf.blank_len, y))
        return None
    return int(x), int(y)


def check_repeat(pl, a, origin, local_pos):
    for p in pl:
        print(p)
        print(get_pos(p[0], origin))
    for p in pl:
        pos = get_pos(p[0], origin)
        if pos is None:
            continue
        x = pos[0]
        if x == 23 and p[1] != a[x + local_pos['_full_times']]:
            return True
    return False


def handle_circle_pos(pList, origin):
    need_update = False
    array = pos_json.get_local_array()
    local_pos = pos_json.get_local_pos()
    local_pos['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 处理最后一列问题
    is_new_col = check_repeat(pList, array, origin, local_pos)

    if is_new_col:
        local_pos['_full_times'] += 1

    for p in pList:
        doOk = False
        pos = get_pos(p[0], origin)
        if pos is None:
            continue
        x = pos[0]
        y = pos[1]

        if p[1] > 0 and is_new_col and x == 23:
            doOk = True
            need_update = True
            x += local_pos['_full_times']
            local_pos['列数'] = x + 1
            array[x][y] = p[1]
            local_pos['小局数'] += 1  # 添加游戏局数
            local_pos[str(local_pos['小局数'])] = print_name_by_value(p[1])

        if p[1] > 0 and array[x][y] == 0 and local_pos['_full_times'] <= 0:
            doOk = True
            need_update = True
            local_pos['列数'] = x + 1
            array[x][y] = p[1]
            local_pos['小局数'] += 1  # 添加游戏局数
            local_pos[str(local_pos['小局数'])] = print_name_by_value(p[1])

        if doOk:
            if y == 1:
                sys_logger.error("下注了......")
            if x - 1 >= 0 and y == 0:
                if (array[x - 1][0] == array[x - 1][1]) and array[x - 1][0] > 0 and array[x - 1][1] > 0 and (
                        array[x - 1][2] == 0):
                    local_pos['成功次数'] += 1  # 符合条件了
                    local_pos['连续失败次数'] = 0  # 失败次数重新计算
                    sys_logger.warning("ok add one")
                else:
                    local_pos['连续失败次数'] += 1
                    if local_pos['连续失败次数'] >= config.conf.fail_times_remind:
                        local_pos['累计连续失败指定次数'] += 1
                        local_pos['连续失败次数'] = 0
                    sys_logger.warning("fail add one")

            if local_pos['成功次数'] >= config.conf.ok_times_remind and (not local_pos['_ok_warning_state']):
                playsound(config.conf.ok_mp3)
                local_pos['_ok_warning_state'] = True
            if local_pos['连续失败次数'] >= config.conf.fail_times_remind and (not local_pos['_fail_warning_state']):
                playsound(config.conf.fail_mp3)
                local_pos['_fail_warning_state'] = True

        # if (p[1] > 0 and array[x][y] > 0) and p[1] != array[x][y] and (not is_new_col):
        #     need_update = True
        #     s = str(local_pos['小局数'])
        #     s += "_"
        #     new_result = "{0}->{1}".format(print_name_by_value(array[x][y]), print_name_by_value(p[1]))
        #     local_pos[s] = new_result
        #     array[x][y] = p[1]
        #     sys_logger.warning(new_result)

    if need_update:
        pos_json.set_local_array(array)
        pos_json.set_local_pos(local_pos)


def fill_pos_array():
    while 1:
        screenshot.window_capture(const.Const.screen_path)
        originScreen = ac.imread(const.ORIGIN_PATH)
        circleScreen = ac.imread(const.RED_CIRCLE_PATH)
        circleScreen2 = ac.imread(const.BLUE_CIRCLE_PATH)
        circleScreen3 = ac.imread(const.HE_RED_CIRCLE_PATH)
        circleScreen4 = ac.imread(const.HE_BLUE_CIRCLE_PATH)
        pos_list.clear()
        try:
            screen = ac.imread(const.Const.screen_path)

            originTemplate = ac.find_template(screen, originScreen, threshold=0.9, rgb=True, bgremove=True)
            if originTemplate is None:
                time.sleep(config.conf.screenshot_main_time)
                continue
            origin = originTemplate['rectangle'][1]
            print(origin)

            template = ac.find_all_template(screen, circleScreen, rgb=True, threshold=config.conf.red_circle_threshold,
                                            bgremove=True)
            if template is not None and len(template) > 0:
                for t in template:
                    pos_list.append((t['rectangle'][0], const.RED_VALUE))

            template2 = ac.find_all_template(screen, circleScreen2, rgb=True,
                                             threshold=config.conf.blue_circle_threshold,
                                             bgremove=True)
            if template2 is not None and len(template2) > 0:
                for t in template2:
                    pos_list.append((t['rectangle'][0], const.BLUE_VALUE))

            template3 = ac.find_all_template(screen, circleScreen3, rgb=True,
                                             threshold=config.conf.he_red_circle_threshold,
                                             bgremove=True)
            if template3 is not None and len(template3) > 0:
                for t in template3:
                    pos_list.append((t['rectangle'][0], const.HE_RED_V))

            template4 = ac.find_all_template(screen, circleScreen4, rgb=True,
                                             threshold=config.conf.he_blue_circle_threshold,
                                             bgremove=True)
            if template4 is not None and len(template4) > 0:
                for t in template4:
                    pos_list.append((t['rectangle'][0], const.HE_BLUE_V))

            new_pos_list = sorted(pos_list, key=lambda x: x[0])
            if len(new_pos_list) > 0:
                handle_circle_pos(new_pos_list, origin)

        except Exception as e:
            sys_logger.error(e)

        time.sleep(config.conf.screenshot_main_time)


def handler_web_close():
    while 1:
        try:
            time.sleep(2)
            screenshot.window_capture(const.Const.screen_path)
            screen = ac.imread(const.Const.screen_path)
            close_screen = ac.imread(const.CLOSE_PATH)
            template = ac.find_template(screen, close_screen, threshold=0.9)
            if template is None:
                continue
            print("页面无投注退出弹框...刷新网页")
            sys_logger.warning("web close...f5")
            win32api.keybd_event(116, 0, 0, 0)  # F5
            win32api.keybd_event(116, 0, win32con.KEYEVENTF_KEYUP, 0)  # Realize the F5 button
        except Exception as e:
            sys_logger.error(e)


def handler_new_game():
    while 1:
        try:
            time.sleep(3)
            screenshot.window_capture(const.Const.screen_path)
            screen = ac.imread(const.Const.screen_path)
            game_start_screen = ac.imread(const.GAME_START_PATH)
            template = ac.find_template(screen, game_start_screen, threshold=0.9)
            if template is None:
                continue
            local_pos = pos_json.get_local_pos()
            if local_pos['列数'] < 24:
                continue
            mv(config.conf.data_save_dir + '//ing.json', "结果")
            mv(config.conf.data_save_dir + '//array_ing.json', "矩阵")
            print("新开一局！！！")
            sys_logger.warning("新开一局")
        except Exception as e:
            sys_logger.error(e)


def mv(src_file, target_name):
    now = datetime.datetime.now()
    if not os.path.isfile(src_file):
        sys_logger.error("src file is not file")
        return
    else:
        target_dir = "{0}\\{1}".format(config.conf.data_save_dir, now.strftime('%Y-%m-%d'))
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        shutil.move(src_file, "{0}\\{1}{2}.json".format(target_dir, now.strftime('%H-%M-%S'), target_name))
    sys_logger.info("保存结果数据")


if __name__ == "__main__":
    # check_circle(const.RED_CIRCLE_PATH, 0.7)
    # check_circle(const.HE_RED_CIRCLE_PATH, 0.8)
    # check_circle(const.HE_BLUE_CIRCLE_PATH, 0.8)
    # check_circle(const.BLUE_CIRCLE_PATH, 0.78)

    # while True:
    #     screenshot.window_capture(const.Const.screen_path)
    #     main_screen = ac.imread(const.Const.screen_path)
    #     findOrigin(main_screen)
    #     time.sleep(config.conf.screenshot_main_time)

    config.conf.handler_config()
    mv(config.conf.data_save_dir + '//ing.json', "结果")
    mv(config.conf.data_save_dir + '//array_ing.json', "矩阵")
    pass
