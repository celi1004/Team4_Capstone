from selenium import webdriver
from .driverutils import DriverUtils
import time

class Options(object):
    KEY = "goog:chromeOptions"
    def __init__(self):
        self._binary_location = ''
        self._arguments = []
        self._extension_files = []
        self._extensions = []
        self._experimental_options = {}
        self._debugger_address = None
        self._caps = DesiredCapabilities.CHROME.copy()



class Naver(object):
    def __init__(self, user_id, user_pw):
        self.ID = user_id
        self.PW = user_pw

        # Web Driver 옵션 추가
        options = webdriver.ChromeOptions()
        #'cookies' : 2, 
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'plugins' : 2, 'popups': 2,
                'geolocation': 2, 'notifications' : 2, 
                'auto_select_certificate': 2, 'fullscreen' : 2, 
                'mouselock' : 2, 'mixed_script': 2, 
                'media_stream' : 2, 'media_stream_mic' : 2, 
                'media_stream_camera': 2, 'protocol_handlers' : 2, 
                'ppapi_broker' : 2, 'automatic_downloads': 2, 
                'midi_sysex' : 2, 'push_messaging' : 2, 
                'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 
                'protected_media_identifier': 2, 'app_banner': 2, 
                'site_engagement' : 2, 'durable_storage' : 2
            }
        }

        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--app=https://google.com") # win32api_login 사용 시 반드시 활성화

        options.add_experimental_option('prefs', prefs)
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")

        # options.add_argument('--headless')

        #options.add_argument("disable-gpu")
        options.add_argument('window-size=1920x1080')
        options.add_argument("lang=ko_KR")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36')
        options.add_argument("user-data-dir=\\user-data\\naver\\")
        self.driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
        # self.driver.get('https://naver.com')
        self.driver.get('https://nid.naver.com/nidlogin.login')

        # time.sleep(1)
        # self.driver.quit()
        # self.driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
        # self.driver.get('https://naver.com')
        #alert 창 닫기
        # alert = self.driver.switch_to_alert()
        # # assert "alert창" in alert.text
        # alert.dismiss()

        self.explicit_wait_time = 0.5
        self.driver_utils = DriverUtils(self.driver)

    def clipboard_login(self, user_id, user_pw):
        # self.driver.find_element_by_xpath('//*[@id="account"]/div/a/i').click()
        time.sleep(0.5)

        self.driver_utils.clipboard_input('//*[@id="id"]', user_id)
        self.driver_utils.clipboard_input('//*[@id="pw"]', user_pw)

        self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

    def win32api_login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="account"]/div/a/i').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="id"]').click()
        self.keyboard.press(list(user_id))
        self.driver.find_element_by_xpath('//*[@id="pw"]').click()
        self.keyboard.press(list(user_pw))
        self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

    def send_keys_login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="account"]/div/a/i').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="id"]').send_keys(user_id)
        self.driver.find_element_by_xpath('//*[@id="pw"]').send_keys(user_pw)
        self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
