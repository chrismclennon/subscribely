import os
import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get("https://accounts.spotify.com/en-US/login")
driver.find_element_by_id("login-username").send_keys("ktperryfan007")
driver.find_element_by_id("login-password").send_keys("tswifty")

login_button = driver.find_element_by_css_selector("button")
login_button.click()

success_notification = driver.find_element_by_xpath("//*[contains(text(), 'You are logged in as ktperryfan007.')]")
print(success_notification.text)

driver.get("https://www.spotify.com/us/purchase/panel/#__main-pci-credit-card")
iframes = driver.find_elements_by_tag_name('iframe')
driver.switch_to.frame(iframes[0])

driver.find_element_by_id("cardnumber").send_keys("1111222233334444")
select(driver.find_element_by_id("expiry-month"), "01")
select(driver.find_element_by_id("expiry-month"), "2020")
driver.find_element_by_id("security-code").send_keys("123")
zip_code = driver.find_element_by_id("zip-code")
zip_code.clear()
zip_code.send_keys("78787")

driver.switch_to_default_content()
payment_button = driver.find_element_by_xpath("//*[contains(text(), 'Start my Spotify Premium')]")
payment_button.click()

error_container = driver.find_element_by_class_name("error-container")
error_notifications = error_container.find_elements_by_tag_name('li')
print("cc_entry errors: " + str(len(error_notifications)))
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
