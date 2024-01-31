from interfaces.projects_computer import ProjectsComputer
import requests


class AccountOrder(ProjectsComputer):
    """
    共享算力订单账户管理
    """
    trade_no = None

    def balance(self):
        """
        获取账户余额
        :return:
        """
        url = f"{self.host}/api/v1/cycle/balance"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def recharge(self):
        """
        唤起订单支付
        :return:
        """
        url = f"{self.host}/api/v1/cycle/recharge"
        payload = {"amount": "0.00", "cycle": 0, "rechargeChannel": 1}
        headers = {'Authorization': self.token,
                   'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, json=payload)
        self.trade_no = response.json()["data"]["outTradeNo"]
        print(response.text)

    def state(self):
        """
        获取支付订单的状态
        :return:
        """
        if self.trade_no is None:
            print("没有唤起支付订单,无发查看支付状态")
            raise Exception
        else:
            url = f"{self.host}/api/v1/cycle/recharge/state?outTradeNo={self.trade_no}"
            headers = {'Authorization': self.token}
            response = requests.request("GET", url, headers=headers)
            print(response.text)
            return response.json()

    def order(self, page, size):
        """
        获取订单列表
        :param page: 页面
        :param size: 页面展示的最大数量
        :return:
        """
        url = f"{self.host}/api/v1/order?page={page}&size={size}"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def transaction(self, pape, size):
        """
        获取充值记录的列表
        :param pape:
        :param size:
        :return:
        """
        url = f"{self.host}/api/v1/cycle/transaction?page={pape}&size={size}"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def redeem_code(self, redeem_code):
        """
        使用兑换码充值
        :param redeem_code: 兑换码
        :return: 兑换充值的结果
        """
        url = f'{self.host}/api/v1/cycle/redeem'
        headers = {'Authorization': self.token}
        data = {"redeemCode": redeem_code}
        response = requests.post(url=url, headers=headers, json=data)
        return response.json()

    def renewal(self, page, size):
        """
        获取续费订单消息
        :param page: 页面
        :param size: 页面的展示数量
        :return:
        """
        url = f"{self.host}/api/v1/cycle/renewal?page={page}&size={size}"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def close(self, rid):
        """
        关闭自动续费
        :param rid:续费订单id
        :return:
        """
        url = f"{self.host}/api/v1/cycle/renewal/{rid}/close"
        payload = {}
        headers = {'Authorization': self.token}
        response = requests.request("PUT", url, headers=headers, json=payload)
        return response.json()

    def open(self, rid):
        """
        打开自动续费
        :param rid: 续费订单id
        :return:
        """
        url = f"{self.host}/api/v1/cycle/renewal/{rid}/open"
        payload = {}
        headers = {'Authorization': self.token}
        response = requests.request("PUT", url, headers=headers, json=payload)
        return response.json()

    def renewal_details(self, cid):
        """
        获取续费订单详情
        :param cid:
        :return:
        """
        url = f"{self.host}/api/v1/cycle/renewal/{cid}"
        headers = {'Authorization': self.token}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def manual_renewal(self, cid):
        """
        对续费订单进行手动续费
        :param cid:
        :return:
        """
        url = f"{self.host}/api/v1/cycle/renewal/{cid}/manual-renew"
        payload = {}
        headers = {'Authorization': self.token}
        response = requests.request("POST", url, headers=headers, json=payload)
        return response.json()

    def call_automatic_renewal(self):
        """
        启动调用自动续费的检索功能
        :return:
        """
        url = f"{self.host}/api/v1/cycle/renewal/daily-check"
        payload = {}
        headers = {'Authorization': self.token}
        response = requests.request("POST", url, headers=headers, json=payload)
        print(response.text)


if __name__ == '__main__':
    ao = AccountOrder('18326447662', 'Dx3826729')
    # # ao.recharge()
    # # ao.state()
    # ao.order(1, 10)
    # ao.open("40e5870c-acaa-4637-9c2c-1fdd2792cc6a")
    # ao.renewal_details("40e5870c-acaa-4637-9c2c-1fdd2792cc6a")
    ao.call_automatic_renewal()
