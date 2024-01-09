import os
import time

import allure
import pytest

from comms.my_ssh_client import MySshClient
from interfaces.cloud_server import CloudServer
from comms.constants import CLOUD_SERVER_INTERFACES, CFI_COMPUTER, DATA_DIR
from comms.log_utils import get_logger
from comms.yaml_utils import get_yaml_data, set_ini_data, get_ini_data, add_yaml_data
from comms.dbutils import DBUtils

logger = get_logger()


@allure.epic('共享算力系统')
@allure.feature("云服务器模块")
@allure.parent_suite('云服务器')
class TestCloudServer:
    cases = get_yaml_data(os.path.join(CLOUD_SERVER_INTERFACES, 'cloud_server.yaml'))  # 读取yaml文件中的测试数据
    cs = CloudServer(cases[0]['case_data']['phone_number'], cases[0]['case_data']['passwd'])

    @allure.suite('云服务器')
    @allure.description("登录账户")
    @pytest.mark.skip("测试通过了")
    def test_login(self):
        case = self.cases[0]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            res = self.cs.test_login(case['case_data']['phone_number'], case['case_data']['passwd'])
            res1 = self.cs.spec()
            res2 = self.cs.image()
            res3 = self.cs.duration()
            assert res['code'] == 200
            assert res1['code'] == 200
            assert res2['code'] == 200
            assert res3['code'] == 200
            assert res['data'] is not None
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    # @pytest.mark.dependency()
    @allure.suite('云服务器')
    @allure.description("创建云服务器")
    @pytest.mark.skip("跳过测试")
    def test_create_computer(self):
        case = self.cases[1]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            res = self.cs.instance_create(case['case_data']['name'], case['case_data']['passwd'])
            set_ini_data(CFI_COMPUTER, 'id', 'computer_id', res['data']['id'])
            assert res['code'] == 200
            assert res['data']['name'] == case['case_data']['name']
            assert res['data']['id'] is not None
            res1 = self.cs.instance()
            assert res1['message'] == 'success'
            self.cs.wait_status(20, res['data']['id'], 1)
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    # @pytest.mark.dependency(depends="TestCloudServer:test_create_computer")
    @allure.suite('云服务器')
    @allure.description("创建端口映射")
    @pytest.mark.skip('暂时跳过')
    def test_create_mapping(self):
        case = self.cases[2]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            computer_id = get_ini_data(CFI_COMPUTER, 'id', 'computer_id')
            res0 = self.cs.page_mapping(1, 10)
            total = res0['data']['total']
            res1 = self.cs.next_mapping(computer_id)
            res = self.cs.mapping_create(computer_id, case['case_data']['port'],
                                         case['case_data']['name'])
            res2 = self.cs.page_mapping(1, 10)['data']['total']
            assert res['code'] == 200
            assert res['networkMapping']['name'] == case['case_data']['name']
            assert res['networkMapping']['id'] is not None
            assert total + 1 == res2
            assert res1['message'] == 'success'
            set_ini_data(CFI_COMPUTER, 'id', 'mapping_id', res['networkMapping']['id'])
            set_ini_data(CFI_COMPUTER, 'mapping', 'public_ip', res1['data']['publicIp'])
            set_ini_data(CFI_COMPUTER, 'mapping', 'public_port', str(res1['data']['publicPort']))
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("验证端口映射")
    @pytest.mark.skip('暂时跳过')
    def test_check_mapping(self):
        case = self.cases[3]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            time.sleep(3)
            public_ip = get_ini_data(CFI_COMPUTER, 'mapping', 'public_ip')
            public_port = get_ini_data(CFI_COMPUTER, 'mapping', 'public_port')
            username = case['case_data']['name']
            passwd = case['case_data']['passwd']
            print(public_ip, public_port, username, passwd)
            mc = MySshClient(public_ip, public_port, username, str(passwd))
            a1, a2, a3 = mc.exec_command('pwd')
            a = a2.read().decode()
            assert 'home' in a
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("删除端口映射")
    @pytest.mark.skip('暂时跳过')
    def test_del_mapping(self, mysql_db):
        case = self.cases[4]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            mapping_id = get_ini_data(CFI_COMPUTER, 'id', 'mapping_id')
            res = self.cs.del_mapping(mapping_id)
            assert res['code'] == 200
            a = mysql_db.find_one('SELECT delete_state FROM network_mappings WHERE id=%s ;', mapping_id)
            assert a[0] == 1
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("访问实例")
    def test_vnc_computer(self):
        case = self.cases[5]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            computer_id = get_ini_data(CFI_COMPUTER, 'id', 'computer_id')
            res = self.cs.vnc(computer_id)
            print(res)
            assert 'https://' in res['data']
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("重启实例")
    @pytest.mark.skip("暂时跳过")
    def test_restart_computer(self, mysql_db):
        case = self.cases[6]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            computer_id = get_ini_data(CFI_COMPUTER, 'id', 'computer_id')
            res = self.cs.restart(computer_id)
            print(res)
            assert res['code'] == 200
            a = mysql_db.find_one('SELECT status FROM compute_instances WHERE id=%s;', computer_id)
            print(a)
            assert a[0] == 5
            self.cs.wait_status(20, computer_id, 1)
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("关闭实例")
    @pytest.mark.skip("暂时跳过")
    def test_stop_computer(self, mysql_db):
        case = self.cases[7]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            computer_id = get_ini_data(CFI_COMPUTER, 'id', 'computer_id')
            res = self.cs.stop(computer_id)
            print(res)
            assert res['code'] == 200
            a = mysql_db.find_one('SELECT status FROM compute_instances WHERE id=%s;', computer_id)
            print(a)
            assert a[0] == 3
            self.cs.wait_status(20, computer_id, 4)
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("启动实例")
    @pytest.mark.skip("暂时跳过")
    def test_start_computer(self, mysql_db):
        case = self.cases[8]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            computer_id = get_ini_data(CFI_COMPUTER, 'id', 'computer_id')
            res = self.cs.start(computer_id)
            print(res)
            assert res['code'] == 200
            a = mysql_db.find_one('SELECT status FROM compute_instances WHERE id=%s;', computer_id)
            print(a)
            assert a[0] == 2
            self.cs.wait_status(20, computer_id, 1)
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('云服务器')
    @allure.description("删除实例")
    @pytest.mark.skip("暂时跳过")
    def test_del_computer(self, mysql_db):
        case = self.cases[8]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.cs.host, name="请求地址")
        try:
            computer_id = get_ini_data(CFI_COMPUTER, 'id', 'computer_id')
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
