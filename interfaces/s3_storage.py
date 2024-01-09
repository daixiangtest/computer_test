from interfaces.projects_computer import ProjectsComputer
import requests
from requests_toolbelt import MultipartEncoder


class S3Storage(ProjectsComputer):
    def user_s3(self):
        """
        查看当前用户的信息创建储存罐是可以data中的name值来为罐命名（name-bucket name）
        :return: 存储罐列表信息
        """
        url = f"{self.host}/api/v1/user"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def create_bucket(self, bucket_name):
        """
        创建存储罐
        :param bucket_name: 罐名称（注意名称格式）
        :return:
        """
        url = f"{self.host}/api/v1/s3bucket"
        payload = f'bucketName={bucket_name}'
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def get_bucket(self, page, size):
        """
        查看当前用户下的存储罐情况
        :param page:
        :param size:
        :return:
        """
        url = f"{self.host}/api/v1/s3bucket?page={page}&size={size}&name="

        payload = {}
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def empty_bucket(self, bucket_name):
        """
        清除存储罐中的文件
        :param bucket_name: 存储罐名称
        :return:
        """
        url = f"{self.host}/api/v1/s3bucket/{bucket_name}/empty"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("DELETE", url, headers=headers)
        return response.json()

    def delete_bucket(self, bucket_name):
        """
        删除储存罐
        :param bucket_name: 储存罐的名称
        :return:
        """
        url = f"{self.host}/api/v1/s3bucket/{bucket_name}"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("DELETE", url, headers=headers)
        return response.json()

    def object_bucket(self, bucket_name, page, size, prefix=""):
        """
        获取存储罐中的文件信息
        :param prefix: 选择需要查看的文件夹路径默认为空只查看罐
        :param bucket_name:罐名称
        :param page:展示的页面
        :param size:每页展示的最大数量
        :return:
        """
        url = f"{self.host}/api/v1/s3bucket/{bucket_name}/objects?prefix={prefix}&page={page}&size={size}&name="
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def upload_s3(self, bucket_name, file_path, file_name=None, file_type=None, prefix=None):
        """
        上传文件至储存罐中
        :param bucket_name: 储存罐的名称
        :param file_path: 上传文件的路径
        :param file_name: 上传后命名的文件名称
        :param file_type: 文件类型
        :param prefix: 选择上传到的文件夹中
        :return:
        """
        url = f"{self.host}/api/v1/storage/{bucket_name}/objects/upload"
        payload = {'prefix': prefix}
        type = None
        if file_name is None:
            file_name = file_path
        if file_type == '.zip' or file_type is None:
            type = 'application/zip'
        elif file_type == '.jpg':
            type = 'image/png'
        elif file_type == '.py' or file_type == '.java':
            type = 'application/octet-stream'
        elif file_type == '.doc':
            type = 'application/msword'
        elif file_type == '.json':
            type = 'application/json'
        elif file_type == '.xlsx':
            type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        files = [('file', (file_name, open(file_path, 'rb'), type)), ]
        headers = {
            'Authorization': self.token
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        return response.json()

    def download_s3(self, bucket_name, file_name):
        """
        下载文件接口
        :param bucket_name: 存储罐名称
        :param file_name: 要下载的文件名
        :return:
        """
        response = None
        try:
            url = f"{self.host}/api/v1/storage/{bucket_name}/objects/download?key={file_name}"
            headers = {'Authorization': self.token}
            response = requests.request("GET", url, headers=headers)
            # open(fr'../datas/{file_name}', 'wb').write(  #将下载的文件保存到本地文件夹中
            #     response.content)
            return response.text

        except Exception as e:
            print('下载接口调用失败', e)
            raise e
        finally:
            response.close()

    def mkdir_s3(self, bucket_name, dirname):
        """
        创建文件夹接口
        :param bucket_name: 存储罐名称
        :param dirname: 文件夹名称
        :return:
        """
        url = f"{self.host}/api/v1/storage/{bucket_name}/mkdir"
        payload = f'dirName={dirname}'
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()


if __name__ == '__main__':
    s3 = S3Storage('18326447662', 'Dx3826729')
    # s3.user_s3()
    # a = s3.create_bucket('18326447662-testddds98')
    # print(a)
    # s3.empty_bucket('18326447662-testddds98')
    # s3.delete_bucket('18326447662-testddds98')
    # s3.object_bucket('18326447662-testddds99', 1, 10)
    # s3.upload_s3('18326447662-testddds99',
    #           r'C:\Users\HUAWEI\Desktop\测试文件大小数据\test02.py', 'test002.py', '.zip')
    a = s3.download_s3('18283-test01', 'test01.py')
    print(a)
    # s3.mkdir_s3('18326447662-testddds99', 'ssst1')
