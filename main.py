# -*- coding: utf-8 -*
__author__ = '张凯'

import json
import argparse

from selenium import webdriver
from selenium.common import  NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
class U8:
    XHR_TYPE = "XHR"
    SUBMISSIONS_URL = "submissions"
    RESPONSE_RECEIVED_METHOD = "Network.responseReceived"

    def __init__(self, nickname, phone, provice, city):
        self.nickname = nickname
        self.phone = phone
        self.provice = provice
        self.city = city

    def select_region(self, browser, name):
        region_dom = browser.find_element(By.XPATH,
                                          '//div[starts-with(@id,"gt-jmy-h5-layer-shell-")]/div[2]/div/div/div[2]')
        region_names = region_dom.find_elements(By.CLASS_NAME, 'form-region-name')
        for i, region_name in enumerate(region_names):
            # print(region_name.text)
            # if region_name.text == name:
            #     region_name.click()
            #     break
            if name in region_name.text:
                time.sleep(1)
                region_name.click()
                break
    def get_clue_id_from_response(self, log, browser):
        log_message = log.get('message', {})
        message_body = log_message.get('message', {})
        if message_body.get("method", "") != self.RESPONSE_RECEIVED_METHOD:
            return None
        params = message_body.get("params", {})
        if params.get("type", "") != self.XHR_TYPE:
            return None
        response = params.get("response", {})
        if not response:
            return None
        url = response.get("url", "")
        if self.SUBMISSIONS_URL not in url:
            return None
        request_jd = params.get("requestId", "")
        if not request_jd:
            return None
        try:
            response_body = browser.execute_cdp_cmd('Network.getResponseBody',
                                                    {'requestId': request_jd})
            return response_body['body']
        except Exception as e:
            # print(f"Error: {e}")
            return None
    def handle(self):
       try:
           caps = DesiredCapabilities.CHROME
           caps['loggingPrefs'] = {
               'browser': 'ALL',
               'performance': 'ALL',
           }
           caps['perfLoggingPrefs'] = {
               'enableNetwork': True,
               'enablePage': False,
               'enableTimeline': False
           }

           # 设置 Chrome 浏览器的驱动程序路径
           driver_path = '/path/to/chromedriver'

           # 初始化 Chrome 浏览器
           options = webdriver.ChromeOptions()
           # driver = webdriver.Chrome(executable_path=driver_path, options=options)
           # 启用performance日志收集
           options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
           # options.add_experimental_option('w3c', False)
           options.add_experimental_option('perfLoggingPrefs', {
               'enableNetwork': True,
               'enablePage': False,
           })
           options.add_argument(
               '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
           )
           options.add_argument('--no-sandbox')
           options.add_argument('--headless')  # 设置无界面模式
           options.add_argument("--disable-extensions")
           options.add_argument("--allow-running-insecure-content")
           options.add_argument("--ignore-certificate-errors")
           options.add_argument("--disable-single-click-autofill")
           options.add_argument("--disable-autofill-keyboard-accessory-view[8]")
           options.add_argument("--disable-full-form-autofill-ios")
           browser = webdriver.Chrome(options=options, desired_capabilities=caps)
           browser.set_window_size(2560, 1440)

           # 访问目标网页
           url = 'https://aisite.wejianzhan.com/site/wjz4cr53/a779d2da-521d-4b34-ae3a-dcfaf36fd91f'
           browser.implicitly_wait(5)
           browser.get(url)

           # 基于索引切换到第 1 个 iframe
           iframe = browser.find_elements(By.XPATH, '/html/body/div/iframe')[0]
           # //*[@id="mip-sjh-trans-form-blank-19822860"]
           # 切换到选择的 iframe
           browser.switch_to.frame(iframe)
           try:
               form_dom = browser.find_element(By.XPATH, '//div[starts-with(@id,"mip-sjh-trans-form-blank-")]')
           except NoSuchElementException:
               print('NO DOM')
           # browser.switch_to.parent_frame()
           # # 找到需要输入的元素
           name_dom = WebDriverWait(browser, 10).until(EC.presence_of_element_located((
               By.XPATH,
               '//div[starts-with(@id,"mip-sjh-trans-form-blank-")]/div/div/div[2]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div/input'
           )))
           # # 模拟用户输入并提交数据
           name_dom.send_keys(self.nickname)

           phone_dom = WebDriverWait(browser, 10).until(EC.presence_of_element_located((
               By.XPATH,
               '//div[starts-with(@id,"mip-sjh-trans-form-blank-")]/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div/input'
           )))
           # # 模拟用户输入并提交数据
           phone_dom.send_keys(self.phone)

           city_dom = WebDriverWait(browser, 10).until(EC.presence_of_element_located((
               By.XPATH,
               '//div[starts-with(@id,"mip-sjh-trans-form-blank-")]/div/div/div[2]/div[1]/div/div[1]/div[3]/div/div[2]/div[1]/div[1]/div/input'
           )))
           # # 模拟用户输入并提交数据
           city_dom.click()
           # //*[@id="gt-jmy-h5-layer-shell-4b534c47-e544-48e2-9d3a-168200567455"]

           region_tab = browser.find_element(By.XPATH,
                                             '//div[starts-with(@id,"gt-jmy-h5-layer-shell-")]/div[2]/div/div/div[1]')
           province_div = region_tab.find_element(By.XPATH, './div[1]')
           province_attr = province_div.get_attribute('class')

           if 'on' in province_attr.split():
               # 第一个div包含class属性为"on"
               # print('省份')
               # #gt-jmy-h5-layer-shell-4b534c47-e544-48e2-9d3a-168200567455 > div.gt-jmy-h5-dialog-custom-dialog-container.is-bottom.mip-sjh-form-picker-bar.vi-picker-bar-skin-select > div > div > div.form-region-scroll > div:nth-child(2)
               # //*[@id="gt-jmy-h5-layer-shell-4b534c47-e544-48e2-9d3a-168200567455"]/div[2]/div/div/div[2]/div[2]
               self.select_region(browser, self.provice)
           # else:
           # 第一个div不包含class属性为"on"
           # print('省份未选中')

           city_div = region_tab.find_element(By.XPATH, './div[2]')
           city_attr = city_div.get_attribute('class')
           if 'on' in city_attr.split():
               # 第一个div包含class属性为"on"
               # print('城市')
               self.select_region(browser, self.city)
           # else:
           # print("城市未选中")
           time.sleep(1)
           # //*[@id="gt-jmy-h5-layer-shell-4b534c47-e544-48e2-9d3a-168200567455"]/div[2]/div/div/div[2]/div[2]
           submit_button = browser.find_element(By.XPATH, '//div[starts-with(@id,"mip-sjh-form-submit-")]/div')
           submit_button.click()
           time.sleep(3)
           logs = browser.get_log('performance')
           resultString = ''
           for log in logs:
              responseBody = self.get_clue_id_from_response(log, browser)
              if responseBody != None:
                  resultString = responseBody
                  break
           print(resultString)
           #
           time.sleep(2)
           #
           # # 输出当前页面标题
           # print(driver.title)
           #
           # 关闭浏览器
           browser.quit()
       except Exception:
            print('')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # pyinstaller main.py   --onefile --specpath ./build/linux
    # python3 main.py --name 张先生 --phone 15536302225 --province 山西 --city  太原
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="客户名称")
    parser.add_argument("--phone", help="手机号")
    parser.add_argument("--province", help="省")
    parser.add_argument("--city", help="市")
    args = parser.parse_args()

    name = args.name
    phone = args.phone
    province = args.province.rstrip("省")
    city = args.city.rstrip("市")
    u8 = U8(name, phone, province, city)
    u8.handle()
