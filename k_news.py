# Coded by Chris Min <infosechris@gmail.com>

import time, pandas, tkinter
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

root = tkinter.Tk()
root.withdraw()
result = tkinter.messagebox.askyesno("Notice", "Do you want to proceed?")

if result:
    #Path for chrome driver and csv file
	url = 'INSERT URL'
	u_id = 'DO NOT INSERT ID IN CODE'
	u_pw = 'DO NOT INSERT PW IN CODE'

    #Go to URL
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    #Select Main Frame
    frame = driver.find_element_by_xpath("//frame[@name='mainFrame']")
    driver.switch_to.frame(frame)

    #Login
    time.sleep(1)
    username = driver.find_element_by_xpath("//*[@id='sns_login_c']/li[1]/input[1]")
    username.send_keys(u_id)
    password = driver.find_element_by_xpath("//*[@id='sns_login_c']/li[1]/input[2]")
    password.send_keys(u_pw)
    driver.find_element_by_xpath("//*[@id='sns_login_c']/li[2]/a/img").click()

    #Select Main Frame again
    time.sleep(1)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//frame[@name='mainFrame']")))
    frame = driver.find_element_by_xpath("//frame[@name='mainFrame']")
    driver.switch_to.frame(frame)

    search = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr[1]/td/table/tbody/tr/td[2]/form/table/tbody/tr/td[2]/input")
    item = "ITEM NAME"
    #Type the item in the search bar and search
    time.sleep(1)
    search.send_keys(item)
    driver.find_element_by_css_selector("img[src='/template/club/skin/basic/images/search_btn.gif']").click()

    #Switching to inner iFrame
    time.sleep(1)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//iframe[@name='club_body']")))
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@name='club_body']"))

    #Click Download, if fails move on
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, item))).click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img[src='/images/board/btn_newDown.gif']"))).click()

else:
    exit