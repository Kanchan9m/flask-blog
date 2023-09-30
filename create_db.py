import mysql.connector as mysqlconnector
mydb = mysqlconnector.connect(
    host="localhost",
    user = "root",
    password = "1234"
)
my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE users")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
