
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re, random

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("http://10.2.0.1:54000")
        driver.find_element_by_id("first-name").click()
        driver.find_element_by_id("first-name").clear()
        driver.find_element_by_id("first-name").send_keys("Administrador")
        driver.find_element_by_id("last-name").clear()
        driver.find_element_by_id("last-name").send_keys("Admin")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("admin@ua.pt")
        driver.find_element_by_id("phone-number").clear()
        driver.find_element_by_id("phone-number").send_keys("123456789")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("adminadmin")
        driver.find_element_by_id("retype-password").clear()
        driver.find_element_by_id("retype-password").send_keys("adminadmin")
        driver.find_element_by_id("company-name").clear()
        driver.find_element_by_id("company-name").send_keys("ua")
        driver.find_element_by_id("company-email").clear()
        driver.find_element_by_id("company-email").send_keys("ua@ua.pt")
        driver.find_element_by_id("company-link").clear()
        driver.find_element_by_id("company-link").send_keys("ua.pt")
        driver.find_element_by_id("install").click()
        while(True):
            try:
                driver.find_element_by_link_text("Services").click()
            except:
                time.sleep(0.5)
                continue
            break
        
        driver.find_element_by_id("service-name").click()
        driver.find_element_by_xpath("//div[@id='filter-services']/div/div/strong").click()
        driver.find_element_by_id("delete-service").click()
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click()

        self.create_service(u"Serviços Académicos - Lic. Mest.")
        self.create_service(u"Serviços Académicos - Dout")
        self.create_service(u"Serviços Académicos - Erasmus")
        self.create_service(u"Serviços Académicos - Prioritário")
        self.create_service(u"Serviços Ação Social - Residências")
        self.create_service(u"Serviços Ação Social - Bolsa de Estudo")

        for i in range(1,50):
            dep = u"Departamento"+str(i)
            self.create_service(dep)
        while(True):
            try:
                driver.find_element_by_link_text("Users").click()
            except:
                time.sleep(0.5)
                continue
            break
        driver.find_element_by_xpath("//div[@id='filter-providers']/div/div").click()
        driver.find_element_by_id("delete-provider").click()
        driver.find_element_by_xpath("(//button[@type='button'])[30]").click()

        for i in range(1,500):
            category1 = str(random.randint(1,56))
            category2 = category1
            while(category2 == category1):
                category2 = str(random.randint(1,56))

            self.create_provider("user"+str(i), category1, category2)
        driver.close()

    def create_service(self, service_name):
        driver = self.driver
        while(True):
            try:
                driver.find_element_by_id("add-service").click()
            except:
                time.sleep(0.5)
                continue
            break
        driver.find_element_by_id("service-name").click()
        driver.find_element_by_id("service-name").clear()
        driver.find_element_by_id("service-name").send_keys(service_name)
        driver.find_element_by_id("service-duration").click()
        driver.find_element_by_id("service-duration").clear()
        driver.find_element_by_id("service-duration").send_keys("10")
        driver.find_element_by_id("service-price").click()
        driver.find_element_by_id("service-price").clear()
        driver.find_element_by_id("service-price").send_keys("0")
        driver.find_element_by_id("service-attendants-number").click()
        driver.find_element_by_id("service-attendants-number").clear()
        driver.find_element_by_id("service-attendants-number").send_keys("1")
        driver.find_element_by_id("service-description").click()
        driver.find_element_by_id("service-description").clear()
        driver.find_element_by_id("service-description").send_keys(u"Escolhe o serviço que queres,")
        driver.find_element_by_xpath("//button[@id='save-service']/span").click()
    
    def create_provider(self, provider_name, provider_category1, provider_category2):
        driver = self.driver
        while(True):
            try:
                driver.find_element_by_id("add-provider").click()
            except:
                time.sleep(0.5)
                continue
            break
        driver.find_element_by_id("provider-first-name").click()
        driver.find_element_by_id("provider-first-name").clear()
        driver.find_element_by_id("provider-first-name").send_keys(provider_name)
        driver.find_element_by_id("provider-last-name").clear()
        driver.find_element_by_id("provider-last-name").send_keys(provider_name)
        driver.find_element_by_id("provider-email").clear()
        driver.find_element_by_id("provider-email").send_keys(provider_name+"@ua.pt")
        driver.find_element_by_id("provider-phone-number").clear()
        driver.find_element_by_id("provider-phone-number").send_keys("123456789")
        driver.find_element_by_id("provider-username").click()
        driver.find_element_by_id("provider-username").clear()
        driver.find_element_by_id("provider-username").send_keys(provider_name)
        driver.find_element_by_id("provider-password").clear()
        driver.find_element_by_id("provider-password").send_keys("useruser")
        driver.find_element_by_id("provider-password-confirm").clear()
        driver.find_element_by_id("provider-password-confirm").send_keys("useruser")
        if provider_category1 == "1":
            driver.find_element_by_xpath("//input[@type='checkbox']").click()
        else:    
            driver.find_element_by_xpath("(//input[@value=''])["+provider_category1+"]").click()
        if provider_category2 == "1":
            driver.find_element_by_xpath("//input[@type='checkbox']").click()
        else:
            driver.find_element_by_xpath("(//input[@value=''])["+provider_category2+"]").click()
        driver.find_element_by_id("save-provider").click()
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()