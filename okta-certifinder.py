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
#driver.get('https://www.credly.com/organizations/okta/directory')

links = parse_csv('okta_consultants_q2_2023.csv')
print(links,end="\n")

for link in links:
    driver.get(link)
    time.sleep(2)

    #needs updating
    developer_cert = driver.find_element(By.XPATH,value="/html/body/main/div[1]/div[2]/div[2]/div/div[5]/div/a/div[2]/div")
    consultant_cert = driver.find_element(By.XPATH,value="/html/body/main/div[1]/div[2]/div[2]/div/div[4]/div/a/div/div")
    admin_cert = driver.find_element(By.XPATH,value="/html/body/main/div[1]/div[2]/div[2]/div/div[3]/div/a/div/div")
    pro_cert = driver.find_element(By.XPATH,value="/html/body/main/div[1]/div[2]/div[2]/div/div[2]/div/a/div/div")

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
        

#searchBox = driver.find_element(By.XPATH,value="/html/body/main/div[1]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div/input")
#searchBox.click()
#earners = driver.find_element(By.XPATH,value="/html/body/main/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div/ul/li[4]/span")
#earners.click()
#searchBox.send_keys("Steven Cenci")
#consultant = driver.find_element(By.XPATH,value="/html/body/main/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div/ul/li")
#consultant.click()




driver.implicitly_wait(2)


# close the browser
driver.quit()
