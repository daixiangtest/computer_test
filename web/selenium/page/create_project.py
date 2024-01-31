import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from comms.constants import CFI
from comms.yaml_utils import get_ini_data
from web.selenium.page.object_page import Computer
from selenium.webdriver import ActionChains
from web.selenium.elenium import elenium as el


class CreateProject(Computer):
    def login_pass(self):
        token = get_ini_data(CFI, "token", "computer")
        self.driver.execute_script(
            f'localStorage.setItem("token","{token}")')
        self.driver.refresh()

    # 验证码登录操作
    def login_phone(self, phone):
        self.send_keys(10, *el.LoginPage.phone, phone)
        self.click(10, *el.LoginPage.Verification_code)
        self.click(10, *el.LoginPage.Terms_of_Service)
        time.sleep(3)
        self.click(10, *el.LoginPage.login_button)

    def add_cookie(self):
        token = get_ini_data(CFI, "token", "computer")
        dict1 = {'domain': '.computeshare.newtouch.com', 'expiry': 1705044061, 'httpOnly': False, 'name': 'token',
                 'path': '/',
                 'sameSite': 'Lax', 'secure': False,
                 'value': token}
        self.driver.add_cookie(dict1)
        self.driver.refresh()

    # 密码登录
    def login_passwd(self, phone, passwd):
        self.click(10, *el.LoginPage.passwd_login)
        self.send_keys(10, *el.LoginPage.phone_ps, phone)
        self.send_keys(10, *el.LoginPage.passwd_ps, passwd)
        self.move_to(3, *el.LoginPage.slider_validation1, *el.LoginPage.slider_validation2, 300)
        self.click(10, *el.LoginPage.Terms_of_Service)
        time.sleep(3)
        self.click(10, *el.LoginPage.login_button)

    # 创建实例
    def create_instance(self, name, passwd):
        self.click(10, *el.CloudServer.create_instance)
        self.send_keys(10, *el.CloudServer.instance_name, name)
        self.send_keys(10, *el.CloudServer.instance_passwd, passwd)
        self.click(10, *el.CloudServer.create_button)

    # 检查实例的启动状态
    def check_status(self, status="运行中"):
        count = 0
        while True:
            time.sleep(3)
            statu = self.text(10, *el.CloudServer.instance_status)
            print(statu)
            if statu == status:
                break
            count += 1
            if count >= 20:
                print("实例状态超时")
                raise TimeoutError
        return True

    # 创建页面的操作
    def create_mapping_page(self, description, port):
        self.click(10, *el.NetworkMapping.create_mapping)
        self.send_keys(10, *el.NetworkMapping.mapping_description, description)
        self.find_elements(10, *el.NetworkMapping.selection)[0].click()
        self.find_elements(10, *el.NetworkMapping.selection_name)[0].click()
        self.find_elements(10, *el.NetworkMapping.selection)[1].click()
        self.find_elements(10, *el.NetworkMapping.selection_name)[1].click()
        self.send_keys(10, *el.NetworkMapping.private_port, port)
        text = self.text(10, *el.NetworkMapping.public_port)
        self.click(10, *el.NetworkMapping.confirm)
        return text


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    # option.add_experimental_option('detach', True)  # 浏览器不会自动关闭
    # remote_url = 'http://192.168.22.238:4444'
    # option.add_argument("--user-data-dir=" + get_ini_data(CFI, 'version', 'chrome_Default'))  # 添加获取到的配置文件路径
    # option.add_experimental_option('detach', True)  # 浏览器不会自动关闭
    # driver = webdriver.Chrome(options=option)  # 打开配置插件的chrome浏览器

    # 配置浏览器选项
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')

    # 连接到远程Selenium Chrome节点
    # driver = webdriver.Remote(command_executor=remote_url, options=chrome_options)
    driver = webdriver.Chrome()  # 打开配置插件的chrome浏览器
    driver.maximize_window()  # 浏览器窗口最大化
    cp = CreateProject(driver)
    cp.geturl('https://computeshare.newtouch.com/login')
    # cp.login_phone(18326447662)
    # ab = driver.caps['goog:chromeOptions']['debuggerAddress']
    # print(ab)
    # time.sleep(3000)
    # cp.login_passwd(18326447662, "Dx3826729")
    cp.login_pass()
    # a = driver.get_cookie("token")
    # print(a)
    a = {'domain': '.computeshare.newtouch.com', 'expiry': 1705044061, 'httpOnly': False, 'name': 'token', 'path': '/',
         'sameSite': 'Lax', 'secure': False,
         'value': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOiI1MzU0YzFhMC1lNmE2LTQzYzctOGI1NC0yZGY1NWNiYzk0MWMiLCJleHAiOjE3MDUwNDQwNjB9.HqmzB2GNKvV3uCA3B_pJmfKSmeJQ3JAvUhHzGrnqFzw'}
    driver.add_cookie(a)
    driver.refresh()
    time.sleep(300)
    driver.quit()
