#!/usr/bin/env python
from selenium import webdriver

# use this instead: "browser = webdriver.Firefox()" if you don't have PhantomJS
browser = webdriver.PhantomJS()

browser.get('http://www.noip.com/login')
username = browser.find_element_by_name('username')
username.send_keys('yourusername')
passwd = browser.find_element_by_name('password')
passwd.send_keys('yourpassword')

loginbtn = browser.find_element_by_name('Login')
loginbtn.submit()

browser.get('http://www.noip.com/members/dns/')
hostdet = browser.find_element_by_class_name('bullet-modify')
hostdet.click()

updatebtn = browser.find_element_by_xpath("//input[@type='submit']")
updatebtn.submit()