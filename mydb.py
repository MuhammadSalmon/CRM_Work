import mysql.connector

dataBase = mysql.connector.connect(
  host='localhost',
  user='admin',
  passwd='Admin1001',
)

# prepare  a cursor object
cursorObject = dataBase.cursor()

# create dataBase

cursorObject.execute("CREATE DATABASE my_db")


print("All done!!")

