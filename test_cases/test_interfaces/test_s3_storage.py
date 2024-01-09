import os

import allure
import pytest
from interfaces.s3_storage import S3Storage
from comms.constants import CLOUD_SERVER_INTERFACES, CFI
from comms.yaml_utils import get_yaml_data, get_ini_data
from comms.log_utils import get_logger

logger = get_logger()


@allure.epic('共享算力系统')
@allure.feature("云服务器模块")
@allure.parent_suite('s3存储')
class TestS3Storage:
    cases = get_yaml_data(os.path.join(CLOUD_SERVER_INTERFACES, 's3_storage.yaml'))  # 读取yaml文件中的测试数据
    s3 = S3Storage(get_ini_data(CFI, 'computer', 'phone'), get_ini_data(CFI, 'computer', 'passwd'))
    # 获取用户名称
    res1 = s3.user_s3()
    name = res1['data']['name']
    bucket_name = name + '-' + cases[0]['case_data']['bucket_name']

    @allure.suite('s3存储')
    @allure.description("创建储存罐")
    # @pytest.mark.skip("测试通过了")
    def test_create_bucket(self, mysql_db):
        case = self.cases[0]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.s3.host, name="请求地址")
        try:

            # 使用用户名——name创建罐的名称
            res2 = self.s3.create_bucket(self.bucket_name)
            assert res2['code'] == 200
            # 数据库验证数据是否到添加到数据库
            count = mysql_db.find_count('SELECT * FROM s3buckets WHERE bucket_name=%s;', self.bucket_name)
            assert count == 1
            # 通过接口查看存储罐是否创建成功
            res3 = self.s3.get_bucket(1, 10)
            bucket_list = res3['data']['list']
            assert self.bucket_name == bucket_list[0]['bucket']
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('s3存储')
    @allure.description("存储罐中创建文件夹")
    # @pytest.mark.skip("测试通过了")
    def test_bucket_mkdir(self):
        case = self.cases[1]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.s3.host, name="请求地址")
        try:
            # 指定罐的名称创建一个文件夹
            res2 = self.s3.mkdir_s3(self.bucket_name, case['case_data']['dir_name'])
            assert res2['code'] == 200
            assert res2['data'] == case['case_data']['dir_name']
            # 查询这个罐信息确认文件夹是否存在
            res3 = self.s3.object_bucket(self.bucket_name, 1, 10)
            dir_list = res3['data']['list']
            assert dir_list[0]['name'] == case['case_data']['dir_name']
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('s3存储')
    @allure.description("存储罐中上传文件")
    # @pytest.mark.skip("测试通过了")
    def test_bucket_upload(self):
        case = self.cases[2]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.s3.host, name="请求地址")
        try:
            # 指定罐的名称创建文件
            res2 = self.s3.upload_s3(self.bucket_name, '../../datas/interfaces/test.py',
                                     file_name=case['case_data']['file_name'], file_type='.py')
            assert res2['code'] == 200
            assert res2['data']['name'] == case['case_data']['file_name']
            # 查询这个罐信息中文件是否存在是否视为一个文件
            res3 = self.s3.object_bucket(self.bucket_name, 1, 10)
            dir_list = res3['data']['list']
            assert dir_list[0]['name'] == case['case_data']['file_name']
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('s3存储')
    @allure.description("储存罐中的文件夹中上传文件")
    # @pytest.mark.skip("测试通过了")
    def test_bucket_upload_dir(self):
        case = self.cases[3]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.s3.host, name="请求地址")
        try:
            # 指定罐的名称的文件中上传文件
            res2 = self.s3.upload_s3(self.bucket_name, '../../datas/interfaces/test.py',
                                     file_name=case['case_data']['file_name'], file_type='.py',
                                     prefix=case['case_data']['dir_name'])
            assert res2['code'] == 200
            assert case['case_data']['dir_name'] and case['case_data']['file_name'] in res2['data']['name']
            # 查询这个罐信息中文件文件夹中文件是否存在
            res3 = self.s3.object_bucket(self.bucket_name, 1, 10, prefix=case['case_data']['dir_name'])
            dir_list = res3['data']['list']
            assert dir_list[0]['name'] == case['case_data']['file_name']
            assert dir_list[0]['prefix'] == case['case_data']['dir_name']
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('s3存储')
    @allure.description("储存罐中的下载文件")
    # @pytest.mark.skip("测试通过了")
    def test_bucket_download(self):
        case = self.cases[4]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.s3.host, name="请求地址")
        try:
            # 指定罐的名称的下载文件获取文件内容
            res2 = self.s3.download_s3(self.bucket_name, file_name=case['case_data']['file_name'])
            assert res2 is not None
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('s3存储')
    @allure.description("清空存储罐")
    # @pytest.mark.skip("测试通过了")
    def test_bucket_empty(self):
        case = self.cases[5]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.s3.host, name="请求地址")
        try:
            # 清空指定罐中的文件
            res2 = self.s3.empty_bucket(self.bucket_name)
            assert res2['code'] == 200
            # 验证罐中的文件是否已经情况
            res3 = self.s3.object_bucket(self.bucket_name, 1, 10)
            assert res3['data']['list'] == []
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e

    @allure.suite('s3存储')
    @allure.description("删除存储罐")
    # @pytest.mark.skip("测试通过了")
    def test_bucket_delete(self, mysql_db):
        case = self.cases[6]
        allure.dynamic.title(case['case_title'])
        allure.attach(body=self.s3.host, name="请求地址")
        try:
            # 删除指定的罐
            res2 = self.s3.delete_bucket(self.bucket_name)
            assert res2['code'] == 200
            # 验证罐是否还存在
            total = self.s3.get_bucket(1, 10)['data']['total']
            res3 = self.s3.get_bucket(1, total)['data']['list']
            for i in res3:
                assert i['bucket'] != self.bucket_name
            # 数据库验证数据是否到添加到数据库
            count = mysql_db.find_count('SELECT * FROM s3buckets WHERE bucket_name=%s;', self.bucket_name)
            assert count == 0
            logger.info(f"测试编号:{case['case_id']},测试标题:{case['case_title']},成功!")
        except Exception as e:
            logger.error(
                f"测试编号:{case['case_title']},测试标题:{case['case_title']},执行失败!", e)
            raise e


if __name__ == '__main__':
    pytest.main(['-vs', __file__])
