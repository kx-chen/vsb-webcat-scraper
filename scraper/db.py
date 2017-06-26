#!/usr/bin/johnsapple

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","","StudentDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute("DROP TABLE STUDENTS;")

# Create table as per requirement
sql = """CREATE TABLE STUDENTS (
		 ID int NOT NULL AUTO_INCREMENT,
		 PRIMARY KEY (ID),
         Student_Number  CHAR(20) NOT NULL,
         Name  CHAR(255) NOT NULL )"""

cursor.execute(sql)

# disconnect from server
db.close()