from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import time
import csv

def parse_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        data = [row["link"] for row in reader]
    return data

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome()

links = parse_csv('okta_consultants_q2_2023.csv') 

#TODO: add csv upload during runtime here.
#TODO: Provide template to end users?
#TODO: CSV may be able to handle URL generation based on firstname and lastname headers

print(links,end="\n")

missing_elements = {}  # dictionary to track missing elements

#TODO: Handle multiple files with same name and date
export_name = "export_okta_certification_dates_" + str(date.today()) + ".csv"

irow = 1
for link in links:
    
    driver.get(link)
    time.sleep(2)

    consultantNameElement = driver.find_element(By.XPATH,value="//*[@id=\"root\"]/div[1]/div[1]/div/div[2]/h1").text
    elements_xpaths = [
        "//a[contains(@title, 'Okta Certified Developer')]",
        "//a[contains(@title, 'Okta Certified Consultant')]",
        "//a[contains(@title, 'Okta Certified Administrator')]",
        "//a[contains(@title, 'Okta Certified Professional')]"
        ]
    
    #TODO: Handle Architect Certification - I think it counts towards both Developer and Consultant paths
    #Start Data Search -- This project will require active housekeeping
    consultantFound = False
    expireBool = False
    for xpath in elements_xpaths:
        try:
            element = driver.find_element(By.XPATH, value=xpath)

            if(xpath == "//a[contains(@title, 'Okta Certified Consultant')]"):
                consultantFound = True

            if element is not None:
                print("clicking element: "+str(element),end="\n")
                time.sleep(1)
                element.click()
                time.sleep(2)

                certificateName = driver.find_element(By.XPATH,value="/html/body/main/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/h1").text        
                issueDateElement = driver.find_elements(By.XPATH,value="/html/body/main/div[1]/div[1]/div/div[2]/p") #TODO: may need to make this more robust for UI changes or other notes.
                expireDateElement = driver.find_elements(By.XPATH,value="/html/body/main/div[1]/div[1]/div/div[2]/span") #TODO: may need to make this more robust for UI changes or other notes.

                if(issueDateElement):
                    issueDate = issueDateElement[0].text
                    print(issueDateElement[0].text,end="\n")
                  
                else:
                    issueDate = 'N/A'

                if(expireDateElement):
                    expireDate = expireDateElement[0].text
                    if('Expired' in expireDate):
                        expireBool = True
                        
                    print(expireDateElement[0].text,end="\n")
                else:
                     expireDateElement = 'N/A'

                driver.back() 
                time.sleep(1)

                with open(export_name,"a",newline='') as file:
                    writer = csv.writer(file)
                    if(irow == 1):
                        writer.writerow(["fullName","certificationName","issueDate","expireDate","Expired"]) #headers
                        irow = irow + 1 

                    if(expireBool):
                        writer.writerow([consultantNameElement,certificateName,issueDate, expireDate,"***"])
                        expireBool = False
                    else:
                        writer.writerow([consultantNameElement,certificateName,issueDate, expireDate])

                #careful with indentation here
                if(consultantFound):
                    break
                    
        except NoSuchElementException:
            print("NoSuchElementException: "+str(xpath),end="\n")
            continue

driver.implicitly_wait(2)
driver.quit()
