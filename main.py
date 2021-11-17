from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome('/home/lakshya/Downloads/chromedriver')
driver.get("http://psd.bits-pilani.ac.in/Login.aspx")
driver.maximize_window()


username = "f20170630@pilani.bits-pilani.ac.in"
password = "45D084FI"
username_path = '//*[@id="TxtEmail"]'
password_path = '//*[@id="txtPass"]'
username_ele = driver.find_element_by_xpath(username_path)
password_ele = driver.find_element_by_xpath(password_path)


username_ele.send_keys(username)
password_ele.send_keys(password)
driver.find_element_by_name("Button1").click()  # Login

prob_bank = '//*[@id="top-navbar"]/ul/li[3]/a'
prob_bank_path = '//*[@id="top-navbar"]/ul/li[3]/ul/li/a'
driver.find_element_by_xpath(prob_bank).click()
driver.find_element_by_xpath(prob_bank_path).click()  # doubt
# time.sleep(10)

rows = driver.find_elements_by_id("prohid")
disciple_path = '//*[@id="Tag"]'
for index, row in enumerate(rows):
    if index > 13:
        stationname = row.find_element_by_id("stationname").text
        location = row.find_element_by_id("lOCATION").text
        stipend = row.find_element_by_id("stipend").text
        print(stationname)
        if len(row.find_element_by_id("viewpro").find_elements_by_tag_name('a')):
            view = row.find_element_by_id("viewpro").click()
            time.sleep(5)
            disciples = driver.find_element_by_xpath(disciple_path).text
            num_projects = driver.find_element_by_id("NoOfProject").text
            print(disciples)
            print("num projects", num_projects)
            # try:
            driver.find_element_by_xpath('//*[@id="panel-close"]').click()
            # except e:
            #     driver.find_element_by_id('panel-close').click()
            print("Exiting.....")
            # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
print(driver.title)
