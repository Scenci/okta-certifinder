from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import tkinter as tk
from tkinter import filedialog
import time
import csv
import os

#prompt for csv file - scoped to be global functions
def prompt_for_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()  
    return file_path

#parse csv file after upload
def parse_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        data = [row["link"] for row in reader]
    return data

class Application(tk.Frame):
    #main
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    #gui
    def create_widgets(self):
        #CSV Upload Button
        self.upload = tk.Button(self)
        self.upload["text"] = "Upload CSV"
        self.upload["command"] = self.upload_file
        self.upload["width"] = 30 #button w
        self.upload["height"] = 10 #button h
        self.upload.pack(side="top")
        self.upload.pack(side="top")

        #Create Template Download Button
        self.templateDL = tk.Button(self)
        self.templateDL["text"] = "Download Template File"
        self.templateDL["command"] = self.download_template
        self.templateDL["width"] = 30
        self.templateDL["height"] = 10
        self.templateDL.pack(side="bottom")
        self.templateDL.pack(side="bottom")

    def download_template(self):
        template_name = "consultant_template_export_name.csv"
        #Check if template already exists
        while os.path.isfile(template_name):
            self.templateDL["text"] = "File already exists in folder!"
            self.templateDL["activebackground"] = "red"
            return

        with open(template_name,"a",newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["firstName","lastName","link"]) #headers
            writer.writerow(["Steven","Cenci","https://www.credly.com/users/steven-cenci/badges?filter%5Buser_name%5D=Steven%20Cenci&source=earner_directory"]) #example user
            file.close
            self.templateDL["text"] = "Done, check the current folder"

        

    def upload_file(self):
        file_path = prompt_for_file()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome()
        #driver = webdriver.Chrome(options=options)
        links = parse_csv(file_path)
        #links = parse_csv('okta_consultants_q2_2023.csv')
        time.sleep(1)
        self.master.destroy()

        #TODO: CSV may be able to handle URL generation based on firstname and lastname headers
        # Examples
        # https://www.credly.com/users/steven-cenci/badges?filter%5Buser_name%5D=Steven%20Cenci&source=earner_directory
        # https://www.credly.com/users/gerald-kusi-mensah/badges?filter%5Buser_name%5D=Gerald%20Kusi-Mensah&source=earner_directory
        # https://www.credly.com/users/neil-malhotra/badges?filter%5Buser_name%5D=Neil%20Malhotra&source=earner_directory
        # Expected issues:
        # If the URL is missed (the name provided is wrong, misspelled, not accurate) - Throw Exception with Continue to next URL attempt...

        print(links,end="\n")

        counter = 1
        base_name = "export_okta_certification_dates_"
        today = str(date.today())
        extension = ".csv"
        export_name = base_name + today + extension

        while os.path.isfile(export_name):
            export_name = base_name + today + "_" + str(counter) + extension
            counter += 1
            print("file with a similar name was found, incrementing file name",end="\n")

        irow = 1
        try:
            for link in links:
                
                driver.get(link)
                time.sleep(2)

                consultantNameElement = driver.find_element(By.XPATH,value="//*[@id=\"root\"]/div[1]/div[1]/div/div[2]/h1").text
                elements_xpaths = [
                    "//a[contains(@title, 'Okta Certified Technical Architect')]",
                    "//a[contains(@title, 'Okta Certified Developer')]",
                    "//a[contains(@title, 'Okta Certified Consultant')]",
                    "//a[contains(@title, 'Okta Certified Administrator')]",
                    "//a[contains(@title, 'Okta Certified Professional')]"
                    ]
                
            
                #Start Data Search -- This project will require active housekeeping
                architectFound = False
                consultantFound = False
                AdminFound = False
                expireBool = False
                for xpath in elements_xpaths:
                    try:
                        element = driver.find_element(By.XPATH, value=xpath)

                        if(xpath == "//a[contains(@title, 'Okta Certified Technical Architect')]"):
                            architectFound = True
                        if(xpath == "//a[contains(@title, 'Okta Certified Consultant')]"):
                            consultantFound = True
                        elif(xpath == "//a[contains(@title, 'Okta Certified Administrator')]"):
                            consultantFound = False
                            AdminFound = True

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

                            if(architectFound):
                                break
                            elif(consultantFound):
                                break
                            elif(AdminFound):
                                break
                    
                    #we need more exception handling - but idk what rn
                    except NoSuchElementException:
                        print("NoSuchElementException: "+str(xpath),end="\n")
                        continue
        finally:
            #TODO FIX: Selenium is hanging after its done, idk why                
            #driver.implicitly_wait(2)
            driver.quit() # the driver is not closing on its own.
        driver.quit()


root = tk.Tk()
root.title('okta-certifinder-v1.1')
root.geometry('500x400')
app = Application(master=root)
app.mainloop()