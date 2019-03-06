from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class NjuVpn(object):
    def __init__(self, user_name, password, chrome_driver=None):
        self.user_name = user_name
        self.password = password
        self.vpn_website = 'https://vpn.nju.edu.cn/dana-na/auth/url_default/welcome.cgi'
        if chrome_driver:
            self.driver = webdriver.Chrome(chrome_driver)
        else:
            self.driver = webdriver.Chrome()
        self.driver.get(self.vpn_website)
        self.__login()
    
    
    def __login(self):
        # 填充表单数据
        username =self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        username.clear()
        password.clear()
        username.send_keys(self.user_name)
        password.send_keys(self.password)

        # 提交用户名、密码以登录
        submit_button = self.driver.find_element_by_name('btnSubmit')
        submit_button.click()

        # 进行异常检测，若此时self.driver.current_url仍为变化，则说明用户名或密码错误
        if self.driver.current_url == self.vpn_website:
            raise ValueError('用户名或密码出现错误，请核实后重新运行本实例。')
        
        # 若此时'p=user-confirm'字段出现在self.driver.current_url中，则说明有另一用户在登录
        if 'p=user-confirm' in self.driver.current_url:
            self.driver.find_element_by_name('btnContinue').click()

        # 登入南京大学VPN系统
        self.driver.find_element_by_xpath('//*[@id="table_webbookmarkline_2"]/tbody/tr/td[2]/a').click()    
