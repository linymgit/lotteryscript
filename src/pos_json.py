import datetime
import json
import os

from src import config, pos


def get_local_pos():
    if os.path.exists(config.conf.data_save_dir + '//ing.json'):
        with open(config.conf.data_save_dir + '//ing.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    else:
        return {
            '房间号': config.conf.root_id,
            '成功次数': 0,
            '连续失败次数': 0,
            '累计连续失败指定次数': 0,
            '列数': 0,
            '小局数': 0,
            '_ok_warning_state': False,
            '_fail_warning_state': False,
            '_full_times': 0,
            'save_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


def set_local_pos(data):
    with open(config.conf.data_save_dir + '//ing.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
        pos.sys_logger.info("更新临时识别结果为：{0}".format(data))


def get_local_array():
    if os.path.exists(config.conf.data_save_dir + '//array_ing.json'):
        with open(config.conf.data_save_dir + '//array_ing.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    else:
        return [[0 for i in range(6)] for j in range(60)]


def set_local_array(array):
    with open(config.conf.data_save_dir + '//array_ing.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(array, ensure_ascii=False, indent=4))
        pos.sys_logger.info("更新矩阵为：{0}".format(array))


if __name__ == "__main__":
    config.conf.handler_config()
    p = get_local_pos()
    p['4'] = 10
    print(p)
    set_local_pos(p)
