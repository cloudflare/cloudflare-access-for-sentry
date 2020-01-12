import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

def std_wait_for_action():
    time.sleep(2)

class SentryPluginEndToEndTest(unittest.TestCase):

    def setUp(self):
        firefox_options = webdriver.FirefoxOptions()
        self.driver = webdriver.Remote(
            command_executor='http://selenium_server:4444/wd/hub',
            options=firefox_options
        )
        self.driver.implicitly_wait(10) # 10 seconds
        self.user_email = "user@testcompany.com"
        self.driver.get("http://securesentry/cdn-cgi/access/auth?email={0}".format(self.user_email))

    def test_login(self):
        std_wait_for_action()
        driver = self.driver
        
        driver.get("http://securesentry/")
        
        sidebar_dropdown = driver.find_element_by_css_selector('[data-test-id="sidebar-dropdown"]')
        assert self.user_email in sidebar_dropdown.text


    def test_logout(self):
        std_wait_for_action()
        driver = self.driver
        
        driver.get("http://securesentry/")
        
        std_wait_for_action()
        sidebar_dropdown = driver.find_element_by_css_selector('[data-test-id="sidebar-dropdown"]')
        sidebar_dropdown.click()
        
        std_wait_for_action()
        signout_elm = driver.find_element_by_css_selector('[data-test-id="sidebarSignout"]')
        signout_elm.click()
                
        # Assertion on the mock server result
        assert "Logout succesful" in driver.page_source

    #TODO test logout

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()