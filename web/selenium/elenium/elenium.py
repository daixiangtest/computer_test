from selenium.webdriver.common.by import By


# 登录页面
class LoginPage:
    # 登录页手机号输入框
    phone = (By.ID, 'phone-register')
    # 获取验证码按钮
    Verification_code = (By.XPATH, '//*[@class="css-3m4nqy ant-btn ant-btn-primary ant-btn-s"]')
    # 确认服务条款
    Terms_of_Service = (By.XPATH, '//*[@class="ant-radio-input"]')
    # 登录按钮
    login_button = (By.XPATH, '//*[@class="css-3m4nqy ant-btn ant-btn-primary ant-btn-l w-full my-[20px]"]')
    # 密码登录字样
    passwd_login = (By.ID, 'rc-tabs-0-tab-2')
    # 密码登录的手机号
    phone_ps = (By.ID, 'phone-login')
    # 密码登录页面的密码验证
    passwd_ps = (By.ID, 'form_item_password')
    # 滑块验证的元素
    slider_validation1 = (By.XPATH, '//*[@class="handler handler_bg"]')
    slider_validation2 = (By.XPATH, '//*[@class="drag_text f14"]')


# 云服务器页面
class CloudServer:
    # 创建实例按钮
    create_instance = (By.XPATH, '//*[@class="css-3m4nqy ant-btn ant-btn-primary ant-btn-s"]')
    # 实例名称输入框
    instance_name = (By.ID, 'form_item_name')
    # 实例密码输入框
    instance_passwd = (By.ID, 'form_item_password')
    # 实例创建按钮
    create_button = (By.XPATH, '//*[@class="css-3m4nqy ant-btn ant-btn-primary ant-btn-m"]')
    # 实例状态
    instance_status = (
        By.XPATH, '//*[@id="rc-tabs-0-panel-1"]/div[2]/div/div/div[1]/div[4]/label[2]')
    # 实例状态选项按钮
    instance_options = (By.XPATH, '//*[@class="w-[28px] cursor-pointer"]')
    # 切换不同的实例状态
    instance_options_number = (By.XPATH, '//*[@class="tips-css"]')
    # 展示的实例名称
    instance_name_page = (By.XPATH, '//*[@class="text-[21px] font-semibold text-ellipsis pr-[15px]"]')
    # vnc输入框
    instance_vnc = (By.XPATH, '//*[@id="screen"]/div/canvas')


# 网络映射页面操作
class NetworkMapping:
    # 点击网络映射按钮
    network_mapping = (By.XPATH, '//*[@id="rc-tabs-0-tab-2"]')
    # 创建映射按钮
    create_mapping = (By.XPATH, '//*[@id="rc-tabs-0-panel-2"]/div/div[1]/button')
    # 映射描述输入框
    mapping_description = (By.XPATH, '//*[@id="basic_des"]')
    # 支持的协议与实例的选择框（0代表协议1代表实例）
    selection = (By.XPATH, '//*[@class="ant-select-selection-item"]')
    # 选择框里面的选项（0代表协议1代表实例）
    selection_name = (By.XPATH, '//*[@class="ant-select-item-option-content"]')
    # 私网端口输入框
    private_port = (By.XPATH, '//*[@id="basic_instancePort"]')
    # 展示的公网端口号
    public_port = (
        By.XPATH, '//*[@id="rc-tabs-0-panel-2"]/div/div[2]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
    # 确认按钮      '//*[@id="rc-tabs-0-panel-2"]/div/div[2]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[5]
    confirm = (By.XPATH, '//*[@class="css-3m4nqy ant-btn ant-btn-primary w-[200px] h-[38px]"]')
    # 删除映射按钮
    delete_mapping = (By.XPATH,
                      '//*[@id="rc-tabs-0-panel-2"]/div/div[2]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[8]/span/span[3]')
    delete_confirm = (By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div/div[2]/button[2]/span')
