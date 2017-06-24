from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

driver = webdriver.Firefox()
driver.get("http://webcat.vsb.bc.ca/ipac20/ipac.jsp?session=&profile=ls&auth=false&submenu=subtab13&date=")

studentID = 811821
while True:
	assert "VSB webcat" in driver.title
	elem = driver.find_element_by_name("sec1")
	elem.clear()
	elem.send_keys(studentID)
	elem.send_keys(Keys.RETURN)

	time.sleep(5)
	logout = driver.find_element_by_class_name("globalAnchor")
	logout.send_keys(Keys.RETURN)

	driver.get("http://webcat.vsb.bc.ca/ipac20/ipac.jsp?session=&profile=ls&auth=false&submenu=subtab13&date=")

	studentID += 1

