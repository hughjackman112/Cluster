# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 12:37:05 2023

@author: PrashanthKotha
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

os.environ['PATH'] += r"C:/SeleniumDriver"
driver = webdriver.Chrome()
driver.get("https://dev-admin-msimga.azurewebsites.net/")
my_email = driver.find_element(by='xpath', value='//*[@id="LoginName"]')
my_email.send_keys('')
my_pw = driver.find_element(by='xpath', value='//*[@id="LoginPassword"]')
my_pw.send_keys('')
my_signin = driver.find_element(by='xpath', value='//*[@id="buttonSignIn"]')
my_signin.click()

products_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Products')]"))
)
driver.execute_script("arguments[0].click();", products_button)

workbooks_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Workbooks')]"))
)
driver.execute_script("arguments[0].click();", workbooks_option)

file_input = driver.find_element(By.ID, 'productworkbookfile')
upload_button = driver.find_element(By.ID, 'buttonUploadWorkbook')

folder_path = 
file_list = os.listdir(folder_path)
uploaded_files = []

for file in file_list:
    dropdown_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "UploadWorkbook_UwCarrierPartyID"))
    )

    dropdown = Select(dropdown_element)
    dropdown.select_by_visible_text("Transverse Specialty Insurance Company")

    file_path = os.path.join(folder_path, file)
    file_input.send_keys(file_path)
    upload_button.click()

    
    timeout = 60
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            success_message = driver.find_element(By.ID, "uploadworkbook-response")
            if success_message.text == "Workbook successfully uploaded":
                uploaded_files.append((file, "Yes"))
                print(f"File '{file}' successfully uploaded.")
                break  
        except:
            pass

        time.sleep(1)

    if time.time() - start_time >= timeout:
        uploaded_files.append((file, "No"))
        print(f"File '{file}' upload failed.")

driver.quit()

print("List of uploaded files:")
for file, status in uploaded_files:
    print(f"{file}: {status}")
