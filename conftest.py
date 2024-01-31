import time

import allure
import pytest
from selenium import webdriver

from comms.constants import CFI
from comms.dbutils import DBUtils
from comms.log_utils import get_logger
from comms.yaml_utils import get_ini_data, set_ini_data
from interfaces.projects_computer import ProjectsComputer


@pytest.fixture(scope="function")
def connect_db():
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    option.add_argument("--user-data-dir=" + get_ini_data('version', 'chrome_Default'))  # 添加获取到的配置文件路径
    option.add_experimental_option('detach', True)  # 浏览器不会自动关闭
    driver = webdriver.Chrome(options=option)  # 打开配置插件的chrome浏览器
    driver.maximize_window()  # 浏览器窗口最大化
    yield driver
    driver.quit()  # 关闭浏览器


@pytest.fixture(scope='function')
def connect_db1():
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()  # 浏览器窗口最大化
    yield driver
    driver.quit()  # 关闭浏览器


@pytest.fixture(scope='function')
def mysql_db():
    db = DBUtils()
    yield db
    db.close()


@pytest.fixture(scope='session', autouse=False)
def set_token():
    try:
        pc = ProjectsComputer.test_login(get_ini_data(CFI, 'computer', 'phone'),
                                         get_ini_data(CFI, 'computer', 'passwd'))
        tk = pc['data']['token']
        set_ini_data(CFI, "token", "computer", tk)
        print("获取token成功")
    except Exception as e:
        print("项目夹具获取token失败")
        get_logger().error("项目夹具获取token失败")
        allure.dynamic.title("项目夹具获取token失败")
        raise e
    yield True
    print("项目测试结束")


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的name和nodeid的中文显示在控制台上
    """
    for i in items:
        i.name = i.name.encode("utf-8").decode("unicode_escape")
        print(i.nodeid)
        i._nodeid = i.nodeid.encode("utf-8").decode("unicode_escape")

# 以上代码的作用是将当前目录下的默认编码unicode更改为utf-8的编码格式这样更加有利于中文的展示
