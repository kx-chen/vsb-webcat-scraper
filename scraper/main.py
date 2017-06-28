#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import MySQLdb
import sys

caps = webdriver.DesiredCapabilities().FIREFOX
caps["marionette"] = False

driver = webdriver.Firefox()

# Open database connection
db = MySQLdb.connect("localhost","root","","StudentDB")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# started at 811000 and 621000

# last 811 number: 814397
# last 621 number: 629601
studentID = int(sys.argv[1])
MASTER_URL = "http://webcat.vsb.bc.ca/ipac20/ipac.jsp?session=&profile=ls&auth=false&submenu=subtab13&date="
LOGIN_URL = "http://webcat.vsb.bc.ca/ipac20/ipac.jsp"

driver.get(MASTER_URL)
studentIdList = open('data/student-id-list', 'w')
nonStudentIdList = open('data/non-student-id-list', 'w')

def logAndPrint(text):
        text = str(text)
        print text
        studentIdList.write(text + '\n')

def waitForPageToLoad():
	time.sleep(0.5)

def writeToFile(studentName, studentID, file):
	studentName = str(studentName)
	studentID = str(studentID)
	sql = "INSERT INTO STUDENTS (Student_Number, Name, Scraped_Date) VALUES ('%s', '%s', '%s');" % (studentID, studentName, time.strftime('%Y-%m-%d %H:%M:%S'))

	if file == 'student-id-list':
		cursor.execute(sql)
		db.commit()


	if file == 'non-student-id-list':
		nonStudentIdList.write(studentID + '\n')

def logout():
	waitForPageToLoad()

	logout = driver.find_element_by_class_name("globalAnchor")
	logout.send_keys(Keys.RETURN)
	driver.get(MASTER_URL)

def login():
        if driver.current_url != LOGIN_URL:
                driver.get(MASTER_URL)
                

	# find login field
	elem = driver.find_element_by_name("sec1")
	elem.clear()
	elem.send_keys(studentID)
	logAndPrint(studentID)
	elem.send_keys(Keys.RETURN)

def getLoggedInName():
	waitForPageToLoad()

	name = driver.find_element_by_xpath("//td[@title='Name']")
	loggedInName = name.get_attribute('innerHTML')

	username = loggedInName.replace("Welcome ", "")
	username = username.replace("&nbsp;", " ")
	username = username.replace(" ", "")
	logAndPrint(username)


while True:
	try: 
		login()
		getLoggedInName()
		logout()

	except:
                logAndPrint("not assigned to anybody.")
		cursor.execute("SELECT * FROM STUDENTS ORDER BY ID DESC LIMIT 1;")

	studentID += 1
	
	if studentID > int(sys.argv[2]):
                driver.quit()
		
        


