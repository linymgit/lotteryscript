import datetime
import json

from src import config

data_dict = {'1': 1, '2': 2, '3': 1, 'name': 'A', 'ok': 1,
             'save_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

config.conf.handler_config()
print(config.conf.data_save_dir)

with open(config.conf.data_save_dir + '//ing.json', 'w+', encoding='utf-8') as f:
    f.write(json.dumps(data_dict, ensure_ascii=False, indent=4))

with open(config.conf.data_save_dir + '//ing.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(data)
