from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import glob
import shutil
from os.path import expanduser
import time
import getpass
import base64
import glob
import os

from selenium.webdriver.common.by import By

def send_user_input(element, value):
    element.clear()
    if value == "username":
        with open("./config/google-config.txt", "r") as config:
            element.send_keys(config.readlines()[0])
    if value == "password":
        with open("./config/google-config.txt", "r") as config:
            password = config.readlines()[1]
        password = base64.b64decode(password)
        element.send_keys(password.decode("ascii"));

def click_xpath(driver, path):
    driver.find_element(By.XPATH, path).click()
    
def click_all_xpaths(driver, path):
    elements = driver.find_elements(By.XPATH, path)
    for element in elements:
        element.click()

# login

options = webdriver.ChromeOptions() 
options.add_argument("download.default_directory=C:\\Users\\cccpo\\Desktop")

driver = webdriver.Chrome("../util/chromedriver/chromedriver.exe", chrome_options=options)

driver.get("https://myaccount.google.com/signin")

assert "Sign in" in driver.title

elem = driver.find_element_by_name("identifier")
send_user_input(element=elem, value="username")
elem.send_keys(Keys.RETURN)

time.sleep(5)

elem = driver.find_element_by_name("password")
send_user_input(element=elem, value="password")
elem.send_keys(Keys.RETURN)

time.sleep(5)


#%% ACCESS 'TAKEOUT LIGHT'

driver.get('https://takeout.google.com/settings/takeout/light')

# uncheck all boxes
click_all_xpaths(driver, "//input[@class='k01p0e kw7Jmf']")
    
# check 'fit' box
click_xpath(driver, 
            "//input[contains(@class, 'k01p0e kw7Jmf') and contains(@value, 'voice')]")

click_xpath(driver, "//input[contains(@class, 'NSt1ae k01p0e')]")



#%% DOWNLOAD LATEST ARCHIVE

print('Waiting 5m for archive to be prepared...')
time.sleep(300)

print('Downloading archive...')
driver.get('https://takeout.google.com/settings/takeout/light')
click_xpath(driver, "//a[contains(., 'Download')]")

if 'Sign in' in driver.title:
    print('Re-entering your password...')
    elem = driver.find_element_by_name("password")
    send_user_input(element=elem, value="password")
    elem.send_keys(Keys.RETURN)

    print('Downloading file...') 
    driver.get('https://takeout.google.com/settings/takeout/light')
    click_xpath(driver, "//a[contains(., 'Download')]")    
    
print('Waiting 5m for download to finish...')
time.sleep(300)

#%% LOGOUT AND CLOSE DRIVER

driver.close()

os.chdir("C:\\Users\\cccpo\\Desktop")


zip_file = glob.glob("takeout*.zip")[0]

parser = HTMLParser();

with gzip.open(zip_file, 'rb') as file_dir:
    os.chdir(file_dir + r"\Takeout\Voice\Calls")
    texting_files = glob.glob("*Text*")
    for file in texting_files:
        parser.feed(file.read())


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)