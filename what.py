from selenium import webdriver
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



driver=webdriver.Chrome()
driver.get('https://web.whatsapp.com/')
input('Enter anything after scanning QR code')


driver.get('https://api.whatsapp.com/send?phone=918897226228&text=You transfered 50/- to Gokul')

ele=driver.find_element_by_id('action-button')
ele.click()
#time.sleep(5)


timeout = 20
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, '_3M-N-'))
    WebDriverWait(driver, timeout).until(element_present)
    element = driver.find_element_by_class_name('_3M-N-')
    driver.execute_script("arguments[0].click();", element)
    
except TimeoutException:
    print("Timed out waiting for page to load")

    



driver.get('https://api.whatsapp.com/send?phone=917779877642&text=You transfered 50/- to Gokul')

ele=driver.find_element_by_id('action-button')
ele.click()



timeout = 20
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, '_3M-N-'))
    WebDriverWait(driver, timeout).until(element_present)
    element = driver.find_element_by_class_name('_3M-N-')
    driver.execute_script("arguments[0].click();", element)
    
except TimeoutException:
    print("Timed out waiting for page to load")

    
