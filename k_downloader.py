from datetime import date
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from termcolor import colored
import time, pandas

#This example requires Selenium WebDriver 3.13 or newer
driver = webdriver.Chrome()

#Go to URL
url = "INSERT URL HERE"
driver.get(url)

#Select Main Frame
frame = driver.find_element_by_xpath("//frame[@name='mainFrame']")
driver.switch_to.frame(frame)

#Login
username = driver.find_element_by_xpath("//*[@id='sns_login_c']/li[1]/input[1]")
username.send_keys("INSERT ID")
password = driver.find_element_by_xpath("//*[@id='sns_login_c']/li[1]/input[2]")
password.send_keys("INSERT PW")
driver.find_element_by_xpath("//*[@id='sns_login_c']/li[2]/a/img").click()

#Select Main Frame again
time.sleep(2)
frame = driver.find_element_by_xpath("//frame[@name='mainFrame']")
driver.switch_to.frame(frame)

#Read CSV file
colnames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
data = pandas.read_csv('media_data.csv', names=colnames, encoding='utf-8')
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

#For While loop counter and failed counter
fcount = 0
wcount = 0
failed = 0

#Go through list, search, and queue it up
search = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr[1]/td/table/tbody/tr/td[2]/form/table/tbody/tr/td[2]/input")
for item in media:
    fcount += 1
    print ("For loop count: " + str(fcount))
    print("Searching and queueing " + str(item) + "...")
    
    #Type the item in the search bar and search
    search.send_keys(item)
    driver.find_element_by_css_selector("img[src='/template/club/skin/basic/images/search_btn.gif']").click()
    time.sleep(1)    
    
    #Switching to inner iFrame
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@name='club_body']"))

    #If element is not displayed, keep clicking the search button
    elem = driver.find_element_by_partial_link_text(item)
    while not (elem.is_displayed() == True):
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_xpath("//frame[@name='mainFrame']"))
        driver.find_element_by_css_selector("img[src='/template/club/skin/basic/images/search_btn.gif']").click()
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@name='club_body']"))
        wcount += 1
        print ("I'm in the while loop!: " + str(wcount))
    
    #Click Download, if fails move on
    try:
        elem.click()
        time.sleep(1)
        driver.find_element_by_css_selector("img[src='/images/board/btn_newDown.gif']").click()
        print("Completed!\n")
    except:
        failed += 1
        print (colored("Failed Queing: ", "red") + colored(str(item), "red") + " !\n")

    #Switch back to Main Frame and clear search bar
    time.sleep(1)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_xpath("//frame[@name='mainFrame']"))
    search.clear()

#Switch back to Homepage when script is done
driver.switch_to.default_content()
driver.get(url)
print ("Total Downloaded: " + str(fcount-failed))