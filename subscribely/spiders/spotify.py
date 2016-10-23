import os
from selenium import webdriver

def select(element, option_text):
    for option in element.find_elements_by_tag_name('option'):
        if option.text == option_text:
            option.click()
            break

def gift_card_status():
    try:
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

        gift_card_status = None
        prepaid_notifications = driver.find_elements_by_xpath("//p[contains(text(), 'Your pre-paid Premium will end on')]")
        nonrecurring_dates = driver.find_elements_by_xpath("//b[@class='nonrecurring-date']")
        if (len(prepaid_notifications) == 1):
            print("gift card is active until " + nonrecurring_dates[0].text)
            gift_card_status = nonrecurring_dates[0].text
        else:
            print("no active gift card found")

        driver.quit()

        return gift_card_status
    finally:
        driver.quit()

def enter_gift_card_code(code):
    try:
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

        driver.find_element_by_id("redeem_code_token").send_keys(code)
        enter_code_button = driver.find_element_by_id("redeem_code_submit")
        enter_code_button.click()

        invalid_notifications = driver.find_elements_by_xpath("//p[contains(text(), 'Unfortunately this Premium code does not seem to be valid')]")
        driver.quit()

        if (len(invalid_notifications) > 0):
            return False
        return True
    finally:
        driver.quit()

def subscribe_with_credit_card_info(ccn, month, year, cvv, zip):
    try:
        month = str(month)
        year = str(year)[-2:]
        cvv = str(cvv)

        print("subscribing with cc... ")
        print("ccn: " + ccn)
        print("month: " + month)
        print("year: " + year)
        print("cvv: " + cvv)
        print("zip: " + zip)

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

        driver.find_element_by_id("cardnumber").send_keys(ccn)
        select(driver.find_element_by_id("expiry-month"), month)
        select(driver.find_element_by_id("expiry-year"), year)
        driver.find_element_by_id("security-code").send_keys(cvv)
        zip_code = driver.find_element_by_id("zip-code")
        zip_code.clear()
        zip_code.send_keys(zip)

        driver.switch_to_default_content()
        payment_button = driver.find_element_by_xpath("//*[contains(text(), 'Start my Spotify Premium')]")
        payment_button.click()

        error_container = driver.find_element_by_class_name("error-container")
        error_notifications = error_container.find_elements_by_tag_name('li')
        print("cc_entry errors: " + str(len(error_notifications)))

        #if (len(error_notifications) > 0):
            #return False
        return True
    finally:
        driver.quit()
