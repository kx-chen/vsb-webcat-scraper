#!/usr/bin/python
# -*- coding: utf-8 -*
import selenium.common.exceptions
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
# last 621 number: 634202
studentID = int(sys.argv[1])
MASTER_URL = "http://webcat.vsb.bc.ca/ipac20/ipac.jsp?session=&profile=ls&auth=false&submenu=subtab13&date="
LOGIN_URL = "http://webcat.vsb.bc.ca/ipac20/ipac.jsp"

driver.get(MASTER_URL)
studentIdList = open('data/student-id-list', 'w')
nonStudentIdList = open('data/non-student-id-list', 'w')

def ensureNotLoggedIn():
        """ returns False if not logged in and True if logged in """
        try:
                driver.find_element_by_link_text("Account Overview")
                return True
                
        except selenium.common.exceptions.NoSuchElementException:
                return False

        else:
                print "Unknown logged in state. Redirecting."
                return True

        
def printAndLog(text):
        text = str(text)
        print text
        studentIdList.write(text + '\n')

def waitForPageToLoad(waitTime):
	time.sleep(waitTime)

def writeToFile(studentName, studentID, file):
	studentName = str(studentName)
	studentID = str(studentID)
	scraped_date = time.strftime('%Y-%m-%d %H:%M:%S')
	scraped_date = str(scraped_date)
	
	sql = """INSERT INTO STUDENTS (Student_Number, Name, Scraped_Date) VALUES ("%s", "%s", "%s");""" % (studentID, studentName, scraped_date)

	if file == 'student-id-list':
		cursor.execute(sql)
		db.commit()


def logout():
	waitForPageToLoad(0.7)
	# globalAnchor is the logout button
	logout = driver.find_element_by_class_name("globalAnchor")
	# click it
	logout.send_keys(Keys.RETURN)
	# go back to home page
	driver.get(MASTER_URL)

def login():
        if driver.current_url != LOGIN_URL:
                # printAndLog("not equal to login_url")
                # printAndLog(driver.current_url)
                driver.get(MASTER_URL)
                

	# find login field
	elem = driver.find_element_by_name("sec1")
	elem.clear()
	elem.send_keys(studentID)
	printAndLog(studentID)
	elem.send_keys(Keys.RETURN)

def getLoggedInName():
	waitForPageToLoad(0.5)

	name = driver.find_element_by_xpath("//td[@title='Name']")
	loggedInName = name.get_attribute('innerHTML')

	username = loggedInName.replace("Welcome ", "")
	username = username.replace("&nbsp;", " ")
	username = username.replace(" ", "")
	printAndLog(username)

	writeToFile(username, studentID, 'student-id-list')


while True:
	try: 
		login()
		getLoggedInName()
		logout()

	except selenium.common.exceptions.NoSuchElementException:
                if ensureNotLoggedIn():
                        driver.get(MASTER_URL)
                printAndLog("Not assigned to anybody.")
		

	studentID += 1
	
	if studentID > int(sys.argv[2]):
                driver.quit()
		
        


