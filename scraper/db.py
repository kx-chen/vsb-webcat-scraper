#!/usr/bin/johnsapple

# --------------------------------
# StudentDB must be created first. 
# ---------------------------------

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","","StudentDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Create table as per requirement
sql = """CREATE TABLE STUDENTS (
		 ID int NOT NULL AUTO_INCREMENT,
		 PRIMARY KEY (ID),
         Student_Number  CHAR(20) NOT NULL,
         Name  CHAR(255) NOT NULL,
	 Scraped_Date CHAR(100) )"""

cursor.execute(sql)

# disconnect from server
db.close()
