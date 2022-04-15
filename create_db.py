# https://www.youtube.com/watch?v=yOmxJbZjTnU&ab_channel=Codemy.com
# https://www.youtube.com/watch?v=hQl2wyJvK5k&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=10&ab_channel=Codemy.com

# pip install mysql-connector
# pip install mysql-connector-python
# pip install mysql-connector-python-rf


import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd = "password123",
)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE our_users")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
	print (db)


## pip install pymysql
## pip install cryptography