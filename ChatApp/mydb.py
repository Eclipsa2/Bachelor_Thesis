import mysql.connector

database = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root123456")

cursor = database.cursor()

cursor.execute("CREATE DATABASE chatapp")
print("Database created successfully")
