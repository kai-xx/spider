# spider
python3+、selenium，通过selenium获取页面元素，实现模拟操作提交。通过记录日志，根据request_id获取接口返回值

通过selenium使用XPATH获取页面元素
通过开启请求日志
  ```
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
           
     ......
           options.add_experimental_option('perfLoggingPrefs', {
               'enableNetwork': True,
               'enablePage': False,
           })
     ......
        logs = browser.get_log('performance')
     ......
     
         response_body = browser.execute_cdp_cmd('Network.getResponseBody',
                                                    {'requestId': request_jd})
            return response_body['body']
     ......
     
  ```
  
