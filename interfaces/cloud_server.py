import time

import requests

from comms.dbutils import DBUtils
from interfaces.projects_computer import ProjectsComputer


class CloudServer(ProjectsComputer):

    def instance_create(self, name, passwd):
        """
        创建云服务器实例
        :param name: 实例名称
        :param passwd: 登录实例的用户名密码，用户名为ubuntu
        :return:
        """
        url = f"{self.host}/api/v1/instance"
        payload = f'duration=1&imageId=1&name={name}&password={passwd}&specId=1'
        headers = {'Authorization': self.token,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def mapping_create(self, computer_id, computer_port, name):
        """
        创建端口映射
        :param computer_id: 创建实例生成的id
        :param computer_port: 创建实例的私网端口号
        :param name: 映射的描述
        :return:
        """
        url = f"{self.host}/api/v1/network-mappings"
        payload = f'computerId={computer_id}&computerPort={computer_port}&name={name}&protocol=TCP'
        headers = {'Authorization': self.token,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def page_mapping(self, page, size):
        """
        查询当前账户所有的端口映射
        :param page: 选择的页面
        :param size: 选择分页的数量
        :return: 所选端口映射的信息
        """
        url = f"{self.host}/api/v1/network-mappings/page?page={page}&size={size}"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def next_mapping(self, computer_id):
        """
        获取实例信息所分配的端口
        :param computer_id: 实例id
        :return: 公网ip与公网端口
        """
        url = f"{self.host}/api/v1/network-mappings/next?computerId={computer_id}"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def del_mapping(self, networking_id):
        """
        删除端口映射
        :param networking_id: 创建端口映射时生成的id
        :return:
        """
        url = f"{self.host}/api/v1/network-mappings/{networking_id}"
        headers = {'Authorization': self.token}
        response = requests.request("DELETE", url, headers=headers)
        return response.json()

    def vnc(self, computer_id):
        """
        访问实例接口
        :param computer_id: 实例id
        :return: 访问实例的url链接
        """
        url = f"{self.host}/api/v1/instance/{computer_id}/vnc"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def restart(self, computer_id):
        """
        重启实例
        :param computer_id: 实例id
        :return:
        """
        url = f"{self.host}/api/v1/instance/{computer_id}/restart"
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
        }
        response = requests.request("PUT", url, headers=headers)
        return response.json()

    def stop(self, computer_id):
        """
        停止实例
        :param computer_id: 实例id
        :return:
        """
        url = f"{self.host}/api/v1/instance/{computer_id}/stop"
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("PUT", url, headers=headers)
        return response.json()

    def start(self, computer_id):
        """
        重启实例
        :param computer_id: 实例id
        :return:
        """
        url = f"{self.host}/api/v1/instance/{computer_id}/start"
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("PUT", url, headers=headers)
        return response.json()

    def wait_status(self, time1, computer_id, status):
        """
        等待加载实例的状态
        :param time1: 等待的时间，3秒一次
        :param computer_id: 创建的实例id
        :param status: 实例的状态，'创建中' = 0,'运行中' = 1,'启动中' = 2,'关闭中' = 3,'已关闭' = 4,'重启中' = 5,'删除中' = 6,'已过期' = 7
        :return:
        """
        count = 0
        while count < time1:
            time.sleep(3)
            db1 = DBUtils()
            b = db1.find_one('SELECT status FROM compute_instances WHERE id=%s;', computer_id)
            print(b)
            db1.close()
            if b[0] == status:
                break
            count += 1
            if count == 20:
                print("实例重启失败或重启时间过长")
                raise AssertionError
        return True


if __name__ == '__main__':
    cc = CloudServer('18326447662', 'Dx3826729')
    a = cc.stop("7ba640dc-d518-4261-ab87-1d9176f3b00d")
    print(a)
