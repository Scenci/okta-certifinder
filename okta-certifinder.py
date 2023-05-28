from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

def parse_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        data = [row["link"] for row in reader]
    return data

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

links = parse_csv('okta_consultants_q2_2023.csv') #TODO: add csv upload during runtime here.
print(links,end="\n")

missing_elements = {}  # dictionary to track missing elements

for link in links:
    driver.get(link)
    time.sleep(2)

    consultantNameElement = driver.find_element(By.XPATH,value="//*[@id=\"root\"]/div[1]/div[1]/div/div[2]/h1")

    #Get the 4 different element types:
    missing_elements[link] = []  # initialize list for this link

    developer_cert = driver.find_elements(By.XPATH, value="//a[contains(@title, 'Okta Certified Developer')]")
    if len(developer_cert) == 0:
        missing_elements[link].append('developer_cert')
    else:
        developer_cert = developer_cert[0]

    consultant_cert = driver.find_elements(By.XPATH,value="//a[contains(@title, 'Okta Certified Consultant')]")
    if len(consultant_cert) == 0:
        missing_elements[link].append('consultant_cert')
    else:
        consultant_cert = consultant_cert[0]

    admin_cert = driver.find_elements(By.XPATH,value="//a[contains(@title, 'Okta Certified Administrator')]")
    if len(admin_cert) == 0:
        missing_elements[link].append('admin_cert')
    else:
        admin_cert = admin_cert[0]

    pro_cert = driver.find_elements(By.XPATH,value="//a[contains(@title, 'Okta Certified Professional')]")
    if len(pro_cert) == 0:
        missing_elements[link].append('pro_cert')
    else:
        pro_cert = pro_cert[0]

    #Start Data Search -- This project will require active maintences most likely.
    #Each time the we do a driver.back() we need to refresh the elements below with their data because the driver gets cleared (stale element error) -- This explains why we are getting an error after the first iteration.
    elements = [developer_cert, consultant_cert, admin_cert, pro_cert]
    for element in elements:
        if element is not None:
            print("clicking element: "+str(element),end="\n")
            time.sleep(2)
            element.click()
            time.sleep(2)
                
            issueDateElement = driver.find_elements(By.XPATH,value="/html/body/main/div[1]/div[1]/div/div[2]/p") #TODO: may need to make this more robust for UI changes or other notes.
            expireDateElement = driver.find_elements(By.XPATH,value="/html/body/main/div[1]/div[1]/div/div[2]/span") #TODO: may need to make this more robust for UI changes or other notes.

            if(issueDateElement is not None):
                print(issueDateElement[0].text,end="\n")
                #Save issueDateElement[0].text to csv file for matching user

            if(expireDateElement is not None):
                print(expireDateElement[0].text,end="\n")
                #Save issueDateElement[0].text to csv file for matching user

            driver.back() 
            time.sleep(2)

print(missing_elements,end="\n")  # print out the missing elements for each link


#Search Logic

    #if(developer cert is not null):
        #get developer cert url
        
        #get developer cert redirect
        #get developer cert issue date
        #get developer cert expiration date
    

    #if(consultant cert is not null):
        #get consultant cert url
        #get consultant cert redirect
        #get consultant cert issue date
        #get consulant cert expiration date
    #elseif(admin cert is not null):
        #get admin cert url
        #get admin cert redirect
        #get admin cert issue date
        #get admin cert expiration date:
        #if (e)xpiration date is <3 months from time.now.date):
            #print("user needs to take recertification exam before expiration date",end="\n")
        #print("user needs to take the next exam level",end="\n")
    #elseif(pro cert is not null):
        #get pro cert url
        #get pro cert redirect
        #get pro cert issue date
        #get pro cert expiration date:
        #print("user needs to take the next exam the next exam level",end="\n")
        



driver.implicitly_wait(2)


# close the browser
driver.quit()
