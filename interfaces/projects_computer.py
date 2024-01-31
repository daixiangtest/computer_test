import time

import requests


class ProjectsComputer:
    token = None
    host = "https://computeshare.newtouch.com"

    def __init__(self, telephone_number, passwd):
        url = f"{self.host}/api/v1/user/login"
        payload = f'countryCallCoding=%2B86&password={passwd}&telephoneNumber={telephone_number}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=payload)
        self.token = "Bearer " + response.json()["data"]["token"]

    @staticmethod
    def test_login(telephone_number, passwd):
        """
        密码登录的静态方法，用于单独测试登录
        :param telephone_number: 手机号
        :param passwd: 密码
        :return: 返回登录状态
        """
        url = "https://computeshare.newtouch.com/api/v1/user/login"
        payload = f'countryCallCoding=%2B86&password={passwd}&telephoneNumber={telephone_number}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def spec(self):
        """
        查询创建实例可选的规格
        :return:
        """
        url = f"{self.host}/api/v1/compute/spec"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def image(self):
        """
        查询创建服务时可选择的系统
        :return:
        """
        url = f"{self.host}/api/v1/compute/image"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    # def duration(self):
    #     """
    #     查询创建实例可以选择的使用时长
    #     :return:
    #     """
    #     url = f"{self.host}/api/v1/compute/duration"
    #     headers = {'Authorization': self.token}
    #     response = requests.request("GET", url, headers=headers)
    #     return response.json()

    def instance(self):
        """
        查询当前账户下的服务器状态
        :return: 返回每个服务器结果
        """
        import requests
        url = f"{self.host}/api/v1/instance"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()


if __name__ == '__main__':
    p = ProjectsComputer('18326447662', 'Dx3826729')
    # print(p.token)
    # a = p.instance()
    # print(a)
