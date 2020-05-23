# Coded by Chris Min <infosechris@gmail.com>
# Note: time.sleep() method is used throughout the code to accomdate chrome process latency. It helps avoiding handling errors.

import time, pandas
from termcolor import colored
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Assign variables
c_path = executable_path='INSERT CHROMEDRIVER PATH'
csv_path= 'INSERT CSV IMPORT PATH'
url = 'INSERT URL'
u_id = 'DO NOT INSERT ID IN CODE'
u_pw = 'DO NOT INSERT PW IN CODE'

#This example requires Selenium WebDriver 3.13 or newer
driver = webdriver.Chrome(c_path)
wait = WebDriverWait(driver, 10)

#Go to URL
driver.get(url)

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

#Read CSV file
colnames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
data = pandas.read_csv(csv_path, names=colnames, encoding='utf-8')
mon = data.Monday.tolist()
tue = data.Tuesday.tolist()
wed = data.Wednesday.tolist()
thr = data.Thursday.tolist()
fri = data.Friday.tolist()
sat = data.Saturday.tolist()
sun = data.Sunday.tolist()

#Update the Media list with current day's items (Without the first item, header)
if date.today().weekday() == 0:
    raw = mon[1:]
elif date.today().weekday() == 1:
    raw = tue[1:]
elif date.today().weekday() == 2:
    raw = wed[1:]
elif date.today().weekday() == 3:
    raw = thr[1:]
elif date.today().weekday() == 4:
    raw = fri[1:]
elif date.today().weekday() == 5:
    raw = sat[1:]
elif date.today().weekday() == 6:
    raw = sun[1:]

#Clean out empty fields from raw file
media = [x for x in raw if str(x) != 'nan']

#For loop counter and try/except failed counter
fcount = 0
failed = 0

#Go through list and download
search = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr[1]/td/table/tbody/tr/td[2]/form/table/tbody/tr/td[2]/input")
for item in media:
    fcount += 1
    print ("For loop count: " + str(fcount))
    print("Searching and queueing " + str(item) + "...")
    
    #Type the item in the search bar and search
    time.sleep(1)
    search.send_keys(item)
    driver.find_element_by_css_selector("img[src='/template/club/skin/basic/images/search_btn.gif']").click()
    
    #Switching to inner iFrame
    time.sleep(1)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//iframe[@name='club_body']")))
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@name='club_body']"))

    #Click Download, if fails move on
    try:
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, item))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img[src='/images/board/btn_newDown.gif']"))).click()
        print("Completed!\n")
    except:
        failed += 1
        print (colored("Failed Queing: ", "red") + colored(str(item), "red") + "\n")

    #Switch back to Main Frame and clear search bar
    time.sleep(1)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_xpath("//frame[@name='mainFrame']"))
    search.clear()

#Switch back to Homepage when script is done
time.sleep(1)
driver.switch_to.default_content()
driver.get(url)
print ("Total Downloaded: " + str(fcount-failed))