from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://www.baidu.com/')

ele = driver.find_element_by_xpath('//p[@class="tang-pass-footerBarULogin pass-link"]')
#
ele.click()