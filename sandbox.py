from selenium import webdriver

# create a new Firefox browser instance
driver = webdriver.Chrome()

# navigate to the Google homepage
driver.get('https://www.google.com')

# print the page title (to confirm that it worked)
print(driver.title)

# close the browser
driver.quit()
