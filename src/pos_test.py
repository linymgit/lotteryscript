import aircv as ac

from src import const

mainScreen = ac.imread("temp/Snipaste_2020-02-29_17-25-28.jpg")
blueCircleScreen = ac.imread(const.BLUE_CIRCLE_PATH)
redCircleScreen = ac.imread(const.RED_CIRCLE_PATH)
origin_screen = ac.imread(const.ORIGIN_PATH)
close_screen = ac.imread(const.CLOSE_PATH)

# template = ac.find_all_template(mainScreen, blueCircleScreen, rgb=False, threshold=0.8)
# print(len(template))
# print(template)

# template = ac.find_all_template(mainScreen, redCircleScreen, rgb=True, threshold=0.7)
# print(len(template))
# print(template)
template = ac.find_template(mainScreen, origin_screen, rgb=True, threshold=0.9)
print(template)