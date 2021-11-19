import json
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains

import time

disciple_path = '//*[@id="Tag"]'


def main():
    with open("data.json", "w") as f:
        cnt = 0
        driver = webdriver.Chrome('/home/lakshya/Downloads/chromedriver')
        driver.get("http://psd.bits-pilani.ac.in/Login.aspx")
        driver.maximize_window()
        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'T')
        # time.sleep(2)
        # action = ActionChains(driver)
        # action.key_down(Keys.CONTROL).send_keys(
        #     Keys.TAB).key_up(Keys.CONTROL).perform()
        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        # time.sleep(3)

        # username = "f20170630@pilani.bits-pilani.ac.in"
        # password = "45D084FI"
        # username_path = '//*[@id="TxtEmail"]'
        # password_path = '//*[@id="txtPass"]'
        # username_ele = driver.find_element_by_xpath(username_path)
        # password_ele = driver.find_element_by_xpath(password_path)

        # username_ele.send_keys(username)
        # password_ele.send_keys(password)
        # driver.find_element_by_name("Button1").click()  # Login

        login(driver)

        prob_bank = '//*[@id="top-navbar"]/ul/li[3]/a'
        prob_bank_path = '//*[@id="top-navbar"]/ul/li[3]/ul/li/a'
        driver.find_element_by_xpath(prob_bank).click()
        driver.find_element_by_xpath(prob_bank_path).click()  # doubt
        # time.sleep(10)

        rows = driver.find_elements_by_id("prohid")
        for index, row in enumerate(rows):
            if cnt % 10 == 0:
                # Open a new window
                driver.execute_script("window.open('');")
                # Switch to the new window and open URL B
                # driver_temp = driver
                driver.switch_to.window(driver.window_handles[1])
                driver.get('http://psd.bits-pilani.ac.in/Login.aspx')
                login(driver)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            try:
                get_project_data(driver, row, f)
                cnt += 1
            except Exception as e:
                driver.execute_script(
                    "window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(2)
                get_project_data(driver, row, f)
                cnt += 1


def login(driver):
    username = "f20170630@pilani.bits-pilani.ac.in"
    password = "45D084FI"
    username_path = '//*[@id="TxtEmail"]'
    password_path = '//*[@id="txtPass"]'
    username_ele = driver.find_element_by_xpath(username_path)
    password_ele = driver.find_element_by_xpath(password_path)

    username_ele.send_keys(username)
    password_ele.send_keys(password)
    driver.find_element_by_name("Button1").click()  # Login


def get_project_data(driver, row, f):
    ps = {}
    # if index > 13:
    stationname = row.find_element_by_id("stationname").text
    location = row.find_element_by_id("lOCATION").text
    stipend = row.find_element_by_id("stipend").text
    print(stationname)

    # ------------------------------------------
    ps["name"] = stationname
    ps["location"] = location
    ps["stipend"] = stipend
    ps["disciplines"] = ""
    ps["no_of_projects"] = ""
    project_list = []

    if len(row.find_element_by_id("viewpro").find_elements_by_tag_name('a')):  # CHECK
        view = row.find_element_by_id("viewpro").click()
        time.sleep(3)
        disciples = driver.find_element_by_xpath(
            disciple_path).text
        num_projects = driver.find_element_by_id(
            "NoOfProject").text
        print("DISCIPLINES", disciples)
        print("NUM. PROJECTS", num_projects)
        ps["disciplines"] = disciples
        ps["no_of_projects"] = num_projects
        current_window_handle = driver.current_window_handle
        driver.find_element_by_xpath('//*[@id="viewProj"]').click()
        # time.sleep(10)
        handles = driver.window_handles
        for handle in handles:
            print(driver.title)
            if handle != current_window_handle:
                driver.switch_to.window(handle)
                time.sleep(3)
                projects = driver.find_elements_by_css_selector(
                    'tbody>div')

                print("No. of Projects", len(projects))

                for index, project in enumerate(projects):
                    # print(project)
                    # if index != len(projects):
                    project_dict = {}
                    title_of_project = project.find_element_by_css_selector(
                        'table tr :nth-child(2)').text

                    description = project.find_element_by_css_selector(
                        'table tr:nth-child(2) :nth-child(2)').text
                    skills = project.find_element_by_class_name(
                        'Skil')
                    # driver.find_element_by_class_name
                    skills = project.find_element_by_css_selector(
                        'table tr:nth-child(3) :nth-child(2)').text
                    print("title :", title_of_project)
                    print("skills: ", skills)

                    project_dict["title"] = title_of_project
                    project_dict["description"] = description
                    project_dict["skills"] = skills
                    project_list.append(project_dict)
                    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                ps["projects"] = project_list

                # writing to file
                f.write(json.dumps(ps))
                f.write(",\n")
                time.sleep(2)
                print("Exiting.....")
                driver.close()
                print("CLOSED")
                driver.switch_to.window(current_window_handle)
                driver.find_element_by_xpath(
                    '//*[@id="panel-close"]').click()


if __name__ == "__main__":
    main()
