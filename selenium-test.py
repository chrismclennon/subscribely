import os
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(5)

driver.get("https://accounts.spotify.com/en-US/login")
driver.find_element_by_id("login-username").send_keys("ktperryfan007")
driver.find_element_by_id("login-password").send_keys("tswifty")

login_button = driver.find_element_by_css_selector("button")
login_button.click()

success_notification = driver.find_element_by_xpath("//*[contains(text(), 'You are logged in as ktperryfan007.')]")
print(success_notification.text)

driver.get("https://www.spotify.com/us/account/subscription/")

prepaid_notifications = driver.find_elements_by_xpath("//p[contains(text(), 'Your pre-paid Premium will end on')]")
nonrecurring_dates = driver.find_elements_by_xpath("//b[@class='nonrecurring-date']")
if (len(prepaid_notifications) == 1):
    print("gift card is active until " + nonrecurring_dates[0].text)
else:
    print("no active gift card found")

#print(driver.page_source)
driver.quit()



driver = webdriver.Chrome()
driver.implicitly_wait(5)

driver.get("https://accounts.spotify.com/en-US/login")
driver.find_element_by_id("login-username").send_keys("ktperryfan007")
driver.find_element_by_id("login-password").send_keys("tswifty")

login_button = driver.find_element_by_css_selector("button")
login_button.click()

success_notification = driver.find_element_by_xpath("//*[contains(text(), 'You are logged in as ktperryfan007.')]")
print(success_notification.text)

driver.get("https://www.spotify.com/us/redeem/prepaid/")

driver.find_element_by_id("redeem_code_token").send_keys("ABCD")
enter_code_button = driver.find_element_by_id("redeem_code_submit")
enter_code_button.click()

invalid_notifications = driver.find_elements_by_xpath("//div[contains(text(), 'Unfortunately this Premium code does not seem to be valid')]")

print(len(invalid_notifications))
driver.quit()
