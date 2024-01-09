import os
import smtplib
import zipfile
from email.mime.text import MIMEText  # 正文用
from email.header import Header  # 标题用
from email.mime.multipart import MIMEMultipart  # 可以用来添加邮件的正文与附件


class SendEmail:
    """
    用来实现对allure生产的文件进行打包压缩然后通过邮箱发送出去
    """

    def __init__(self, fujian_name, dirpath, outFullName):
        """
        :param fujian_name: 需要发送的附近文件地址与文件名称
        :param dirpath: 需要进行压缩的文件地址与文件名称
        :param outFullName: 压缩后的文件所存放的路径与名称
        """
        self.fujian_name = fujian_name
        self.dirpath = dirpath
        self.outFullName = outFullName

    def run(self, addreSsee):
        """
        :param addreSsee:收件人的邮箱地址，发送多个邮件地址时以列表形式存在
        :return:
        """
        send_User = "983643937@qq.com"  # 邮箱地址
        send_Password = "njwzjuklcjwibbha"  # 163邮箱的smtp密码
        send_Smtp = "smtp.qq.com"  # 使用的邮箱smtp官方地址
        addreSsee = addreSsee  # 收件箱地址
        # 规定邮件的内容
        text = """       
邮件通知:
<html>
<head>
    <meta charset="UTF-8">
    <title>Hamster自动化测试报告</title>
</head>

<body leftmargin="8" marginwidth="0" topmargin="2" marginheight="4"
      offset="0">
<table width="95%" cellpadding="0" cellspacing="0"
       style="font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
    <tr>
        本邮件为hamster自动化测试报告邮件，由系统自动发出，无需回复！<br/>
        各位领导，同事，大家好，以下为附近文件为Hamster项目自动化检查报告</br>
        此自动化框架依赖python3开发环境，自动化框架pytest以及相关的开发工具Allure等</br>
        allure测试报告需要依赖allure环境来打开，您可以下载附件的压缩文件包解压到您的本地文件夹中</br>
        <td><font color="#CC0000">构建结果：点击reports文件包中的look_allure文件来打开allure报告内容</font></td>
    </tr>
</table>
</div>
<br/>
<tr>
    <td>
        <br/>
        <b>
            <font color="red" size="2"> 详细内容见测试报告：请下载附件查看</font>
        </b>
    </td>
</tr>
</table>
<tr>
</tr>
</body>
</html>
"""
        # 创建一个MIMEMultipart的对象来发送邮件
        msg = MIMEMultipart()
        # 添加邮件的内容，文本格式为HTML格式
        msg.attach(MIMEText(text, 'html', 'utf-8'))
        # msg = MIMEText('hh', 'base64', 'utf-8')  # 数据编码方式是utf-8
        # 获取需要上传的文件上传到邮箱的附件中
        hh = open(self.fujian_name, 'rb').read()
        att1 = MIMEText(hh, "base64", "utf-8")
        # 规定数据的传输类型
        att1['Content-Type'] = 'application/octet-stream'
        # 定义上传文件的文件名称和后缀名
        att1["Content-Disposition"] = 'attachment; filename=' + self.fujian_name
        msg.attach(att1)
        # 第一种发件人方式：
        msg['From'] = send_User  # 显示邮件的发件问信息
        # print(type(msg['From']))  # 是一个email的对象
        msg['Subject'] = Header(u'Hamster自动化测试报告', 'utf-8').encode()  # 邮件的主题 u一般用在中文字符串前面，防止因为源码储存格式问题
        msg['To'] = u'Hamster项目组'  # 显示的收件人的名字（自定义）
        # print(msg)  # 打印发送给接受的数据
        # print(type(msg))
        # 实例化一个邮箱对象
        smtp = smtplib.SMTP()
        smtp.connect(send_Smtp, 25)  # 这是发送出去的邮箱的smtp的地址和默认端口
        smtp.login(send_User, send_Password)  # 这是登录的账号和smtp密码，用于除了网页以外的客户端登录
        # 发送邮件，传入发送账号，接收账号，将设置好的邮件主题传入
        smtp.sendmail(send_User, addreSsee, msg.as_string())
        smtp.quit()  # 关闭连接

    def zipDir(self):
        # 获取文件进行文件压缩
        zip = zipfile.ZipFile(self.outFullName, "w", zipfile.ZIP_DEFLATED)
        # 对需要压缩的文件进行遍历
        for path, dirnames, filenames in os.walk(self.dirpath):
            # 去掉目录跟路径，只对目录文件夹下边的文件及文件夹本身进行压缩
            fpath = path.replace(self.dirpath, '')
            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()


if __name__ == '__main__':
    # 调试尝试一下是否调通
    a = SendEmail('report.html', r'send_dir', r"send_dir.zip")
    a.run(["983643937@qq.com", "1144607112@qq.com"])
