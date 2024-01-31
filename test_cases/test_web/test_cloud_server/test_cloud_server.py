import os

import allure
import time
import pytest
from selenium.webdriver.common.by import By
from comms.constants import CLOUD_SERVER_WEB, CFI, DATA_DIR
from comms.log_utils import get_logger
from comms.yaml_utils import get_yaml_data, get_picture, get_ini_data, set_ini_data, add_yaml_data
from interfaces.cloud_server import CloudServer
from web.selenium.page.create_project import CreateProject
from web.selenium.elenium import elenium as em
from comms.my_ssh_client import MySshClient

logger = get_logger()


@allure.epic('共享算力系统')
@allure.feature("云服务器模块")
@allure.parent_suite('云服务器')
class TestCloudServer:
    cases = get_yaml_data(os.path.join(CLOUD_SERVER_WEB, 'cloud_server.yaml'))  # 读取yaml文件中的测试数据

    @allure.suite('云服务器')
    @allure.description("登录账户")
    @pytest.mark.skip("测试通过了")
    def test_login(self, connect_db1):
        cp = CreateProject(connect_db1)
        case = self.cases[0]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            # 输入链接地址
            cp.geturl(get_ini_data(CFI, 'computer', 'url'))
            # 登录账户
            cp.login_passwd(get_ini_data(CFI, 'computer', 'phone'), get_ini_data(CFI, 'computer', 'passwd'))
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
    def test_create_instance(self, connect_db1):
        case = self.cases[1]
        cp = CreateProject(connect_db1)
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            cp.geturl(get_ini_data(CFI, 'computer', 'url'))
            cp.login_pass()
            # 创建实例
            cp.create_instance(case['case_data']['name'], case['case_data']['passwd'])
            time.sleep(3)
            # 检查实例的状态是否创建成功
            cp.check_status()
            # 获取创建的实例名称
            text = cp.find_elements(10, *em.CloudServer.instance_name_page)[0].text
            assert text == case['case_data']['name']
            logger.info(f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行成功！")
        except Exception as e:
            get_picture(connect_db1, "创建云服务器失败截图")  # 失败截图
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("创建网络端口")
    @pytest.mark.skip("测试通过了")
    def test_create_port(self, connect_db1):
        case = self.cases[2]
        cp = CreateProject(connect_db1)
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            cp.geturl(get_ini_data(CFI, 'computer', 'url'))
            cp.login_pass()
            # 点击端口映射
            cp.click(10, *em.NetworkMapping.network_mapping)
            # 点击创建端口映射
            text = cp.create_mapping_page(case['case_data']['description'], case['case_data']['port'])
            set_ini_data(CFI, 'instance', 'port', text)
            logger.info(f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行成功！")
        except Exception as e:
            get_picture(connect_db1, "创建云服务器失败截图")  # 失败截图
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("验证网络端口")
    @pytest.mark.skip("测试通过了")
    def test_check_port(self):
        case = self.cases[3]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            # 获取服务器的链接信息
            time.sleep(3)
            public_ip = get_ini_data(CFI, 'instance', 'ip')
            public_port = get_ini_data(CFI, 'instance', 'port')
            username = case['case_data']['name']
            passwd = case['case_data']['passwd']
            print(public_ip, public_port, username, passwd)
            mc = MySshClient(public_ip, public_port, username, str(passwd))
            a1, a2, a3 = mc.exec_command('pwd')
            a = a2.read().decode()
            print(a)
            assert 'home' in a
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("删除网络端口")
    @pytest.mark.skip("测试通过了")
    def test_delete_port(self, connect_db1):

        case = self.cases[4]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            cp = CreateProject(connect_db1)
            # 获取服务器的链接信息
            public_port = get_ini_data(CFI, 'instance', 'port')
            cp.geturl(get_ini_data(CFI, 'computer', 'url'))
            cp.login_pass()
            cp.click(10, *em.NetworkMapping.network_mapping)
            # 删除端口映射
            pp = cp.text(10, *em.NetworkMapping.public_port)
            print(pp)
            if pp == public_port:
                cp.click(10, *em.NetworkMapping.delete_mapping)
                cp.click(10, *em.NetworkMapping.delete_confirm)
            time.sleep(3)
            pp = cp.text(10, *em.NetworkMapping.public_port)
            print(pp)
            assert pp != public_port
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("访问实例")
    @pytest.mark.skip("测试通过了")
    def test_access_instance(self, connect_db1):

        case = self.cases[5]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            cp = CreateProject(connect_db1)
            # 获取服务器的链接信息
            cp.geturl(get_ini_data(CFI, 'computer', 'url'))
            cp.login_pass()
            cp.add_cookie()
            # 点击访问实例
            name = cp.find_elements(10, *em.CloudServer.instance_name_page)[0].text
            print(name)
            assert case['case_data']['name'] == name
            cp.find_elements(10, *em.CloudServer.instance_options)[0].click()
            cp.find_elements(10, *em.CloudServer.instance_options_number)[0].click()
            time.sleep(3)
            cp.window(1)
            res = cp.iselement(5, *em.CloudServer.instance_vnc)
            print(res)
            assert res
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("重启实例")
    @pytest.mark.skip("测试通过了")
    def test_restart_instance(self, connect_db1):

        case = self.cases[6]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            cp = CreateProject(connect_db1)
            # 获取服务器的链接信息
            public_port = get_ini_data(CFI, 'instance', 'port')
            cp.geturl(get_ini_data(CFI, 'computer', 'url'))
            cp.login_pass()
            # 点击访问实例
            name = cp.find_elements(10, *em.CloudServer.instance_name_page)[0].text
            print(name)
            assert case['case_data']['name'] == name
            cp.find_elements(10, *em.CloudServer.instance_options)[0].click()
            cp.find_elements(10, *em.CloudServer.instance_options_number)[1].click()
            time.sleep(1)
            starts = cp.text(10, *em.CloudServer.instance_status)
            print(starts)
            assert starts == case['case_data']['starts']
            assert cp.check_status()
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("关闭实例")
    @pytest.mark.skip("测试通过了")
    def test_stop_instance(self, connect_db1):
        case = self.cases[7]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            cp = CreateProject(connect_db1)
            # 获取服务器的链接信息
            public_port = get_ini_data(CFI, 'instance', 'port')
            cp.geturl(get_ini_data(CFI, 'computer', 'url'))
            cp.login_pass()
            # 点击访问实例
            name = cp.find_elements(10, *em.CloudServer.instance_name_page)[0].text
            print(name)
            assert case['case_data']['name'] == name
            cp.find_elements(10, *em.CloudServer.instance_options)[0].click()
            cp.find_elements(10, *em.CloudServer.instance_options_number)[2].click()
            time.sleep(1)
            starts = cp.text(10, *em.CloudServer.instance_status)
            print(starts)
            assert starts == case['case_data']['starts']
            assert cp.check_status("已关闭")
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("关闭实例")
    @pytest.mark.skip("测试通过了")
    def test_start_instance(self, connect_db1):
        case = self.cases[8]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            cp = CreateProject(connect_db1)
            # 获取服务器的链接信息
            public_port = get_ini_data(CFI, 'instance', 'port')
            cp.geturl(get_ini_data(CFI, 'computer', 'url'))
            cp.login_pass()
            # 点击访问实例
            name = cp.find_elements(10, *em.CloudServer.instance_name_page)[0].text
            print(name)
            assert case['case_data']['name'] == name
            cp.find_elements(10, *em.CloudServer.instance_options)[0].click()
            cp.find_elements(10, *em.CloudServer.instance_options_number)[0].click()
            time.sleep(1)
            starts = cp.text(10, *em.CloudServer.instance_status)
            print(starts)
            assert starts == case['case_data']['starts']
            assert cp.check_status()
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("删除实例")
    # @pytest.mark.skip("暂时跳过")
    def test_del_instance(self, mysql_db):
        case = self.cases[9]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=get_ini_data(CFI, "computer", "url"), name="请求地址")
        try:
            cs = CloudServer(get_ini_data(CFI, 'computer', 'phone'), get_ini_data(CFI, 'computer', 'passwd'))
            pc = cs.instance()
            print(pc)
            name = pc['data'][0]['name']
            assert name == case['case_data']['name']
            computer_id = pc['data'][0]['id']
            a = mysql_db.cud('DELETE FROM compute_instances WHERE id=%s;', (computer_id,))
            assert a == 1
            add_yaml_data(os.path.join(DATA_DIR, 'computer_id.yaml'), computer_id)
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e


if __name__ == '__main__':
    pytest.main(['-vs', __file__])
