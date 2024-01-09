import allure
import time
import pytest
from selenium.webdriver.common.by import By
from comms.constants import CLOUD_SERVER
from comms.log_utils import get_logger
from comms.yaml_utils import get_yaml_data, get_picture, get_ini_data, set_ini_data
from web.selenium.page.create_project import CreateProject
from web.selenium.elenium import elenium as em
from comms.my_ssh_client import MySshClient

logger = get_logger()


@allure.epic('共享算力系统')
@allure.feature("云服务器模块")
@allure.parent_suite('云服务器')
class TestCloudServer:
    cases = get_yaml_data(CLOUD_SERVER)  # 读取yaml文件中的测试数据

    @allure.suite('云服务器')
    @allure.description("登录账户")
    @pytest.mark.skip("测试通过了")
    def test_login(self, connect_db1):
        cp = CreateProject(connect_db1)
        case = self.cases[0]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data("computer", "url"), name="请求地址")
        try:
            # 输入链接地址
            cp.geturl(get_ini_data('computer', 'url'))
            # 登录账户
            cp.login_passwd(get_ini_data('computer', 'phone'), get_ini_data('computer', 'passwd'))
            # 获取网页标题
            title = connect_db1.title
            assert title == "共享算力"
            time.sleep(3)
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
            time.sleep(3)
            # print(connect_db1.caps['goog:chromeOptions']['debuggerAddress'])
            # time.sleep(3000)
        except Exception as e:
            get_picture(connect_db1, "登录失败图片")  # 失败截图
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            logger.exception(e)
            raise e

    @allure.suite('云服务器')
    @allure.description("创建云服务器")
    @pytest.mark.skip("测试通过了")
    def test_create(self, connect_db1):
        case = self.cases[1]
        cp = CreateProject(connect_db1)
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data("computer", "url"), name="请求地址")
        try:
            # 创建实例
            cp.create_instance(case['case_data']['name'], case['case_data']['passwd'])
            time.sleep(3)
            # 检查实例的状态是否创建成功
            cp.check_status()
            # 获取创建的实例名称
            text = cp.find_elements(10, *em.CloudServer.instance_name_page)[0].text
            assert text == case['case_data']['name']
            logger.info(f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行成功！")
            print(connect_db1.caps['goog:chromeOptions']['debuggerAddress'])
            time.sleep(3000)
        except Exception as e:
            get_picture(connect_db1, "创建云服务器失败截图")  # 失败截图
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("创建云服务器")
    @pytest.mark.skip("测试通过了")
    def test_create_port(self, connect_db1):
        case = self.cases[2]
        cp = CreateProject(connect_db1)
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data("computer", "url"), name="请求地址")
        try:
            # 点击端口映射
            cp.click(10, *em.NetworkMapping.network_mapping)
            # 点击创建端口映射
            text = cp.create_mapping_page(case['case_data']['description'], case['case_data']['port'])
            set_ini_data('instance', 'port', text)
            logger.info(f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行成功！")
            print(connect_db1.caps['goog:chromeOptions']['debuggerAddress'])
            time.sleep(3000)
        except Exception as e:
            get_picture(connect_db1, "创建云服务器失败截图")  # 失败截图
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("创建云服务器")
    # @pytest.mark.skip("测试通过了")
    def test_check_port(self, connect_db1):
        case = self.cases[3]
        cp = CreateProject(connect_db1)
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data("computer", "url"), name="请求地址")
        try:
            # 获取服务器的链接信息
            port = get_ini_data('instance', 'port')
            ip = case["case_data"]['ip']
            name = case["case_data"]['name']
            pwd = case["case_data"]['passwd']
            mc = MySshClient(ip, port, name, pwd)
            text = mc.exec_command("pwd")
            stdin, stdout, stderr = text
            res = stdout.read().decode()
            assert name in res
        except Exception as e:
            get_picture(connect_db1, "创建云服务器失败截图")  # 失败截图
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e


if __name__ == '__main__':
    pytest.main(['-vs', __file__])
