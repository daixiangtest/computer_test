import time, yaml
from configparser import ConfigParser
from comms.constants import PICTURE_DIR, CFI, CFI_COMPUTER
import allure
from selenium import webdriver

"""读取yaml文件数据"""


def get_yaml_data(file):  # 读取yaml文件数据
    try:
        with open(file, mode='r', encoding='utf-8') as fr:
            cases = yaml.safe_load(fr)
            return cases
    except Exception as e:
        print("yaml文件读取失败", e)


def add_yaml_data(file, data):
    try:
        with open(file, mode='a', encoding='utf-8') as fw:
            yaml.safe_dump(data, fw, sort_keys=False, allow_unicode=True)
    except Exception as e:
        print(f"添加数据至{file}失败", e)


# 保存截图
def get_picture(browser, name):
    try:
        # 获取时间戳用来命名截图
        sys_time = time.strftime("%Y%m%d%H%M%S")
        timestamp = int(time.time())
        # 截图名称：时间+截图名字描述+后缀
        png_name = sys_time + name + ".png"
        # 截图存放位置
        png_file = PICTURE_DIR + '\\' + png_name
        page_source_path = PICTURE_DIR + '\\' + sys_time + name + '.html'
        # 获取截图（这才是灵魂）
        browser.save_screenshot(png_file)
        with open(page_source_path, "w", encoding="u8") as f:
            f.write(browser.page_source)
        time.sleep(1)
        allure.attach.file(png_file, name='image', attachment_type=allure.attachment_type.PNG)
        allure.attach.file(page_source_path, name="page_source", attachment_type=allure.attachment_type.HTML)
    except Exception as e:
        print('截图失败', e)


# 读取conf中的config.ini文件
def get_ini_data(path, section, option):
    try:
        cp = ConfigParser()  # 创建 解析器对象
        cp.read(path, encoding="utf-8")  # 加载ini文件
        return cp.get(section, option)  # 通过 标头和选项获取对应的值
    except Exception as e:
        print("从ini文件中读取数据失败", e)
        raise e


def set_ini_data(path, section, option, value):
    try:
        config = ConfigParser()
        config.read(path, encoding="utf-8")
        config.set(section, option, value)
        config.write(open(path, "w"))
        return True
    except Exception as e:
        print("写入文件到init中失败")
        raise e


if __name__ == '__main__':
    # a = get_ini_data("computer", "passwd")
    # print(a)

    set_ini_data(CFI_COMPUTER, "id", 'computer_id', 'aaaa1')
    # set_ini_data("token", "hamster", "112aaassssxx@@@233111")
