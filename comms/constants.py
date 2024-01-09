import os

"""
使用常量对路径进行管理
好处: 代码使用非绝对路径,可移植性高
"""

# 获取项目路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 测试用例执行文件所在路径
CASE_DIR = os.path.join(BASE_DIR, r'test_cases')
CASE_LOGIN = os.path.join(CASE_DIR, r'test_login\test_login.py')
# 测试数据所在路径
DATA_DIR = os.path.join(BASE_DIR, 'datas')
CLOUD_SERVER_WEB = os.path.join(DATA_DIR, 'web')
CLOUD_SERVER_INTERFACES = os.path.join(DATA_DIR, 'interfaces')
# log所在路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')
INFO_FILE = os.path.join(LOG_DIR, 'info.log')
ERROR_FILE = os.path.join(LOG_DIR, 'error.log')

# 测试报告所在路径
REPORT_DIR = os.path.join(BASE_DIR, 'reports')
REPORT_JSON = os.path.join(REPORT_DIR, 'allure_json')
REPORT_HTML = os.path.join(REPORT_DIR, 'allure_html')

# 测试截图所在路径
PICTURE_DIR = os.path.join(BASE_DIR, 'picture')

# 获取config.ini目录
CFI = os.path.join(BASE_DIR, 'confs/confing.ini')
CFI_COMPUTER = os.path.join(BASE_DIR, 'confs/cloud_server.ini')
if __name__ == '__main__':
    print(CLOUD_SERVER_INTERFACES)
    print(CASE_DIR)
    print(REPORT_DIR)
