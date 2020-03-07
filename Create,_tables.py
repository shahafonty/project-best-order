import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")

cursor = db.cursor()

cursor.execute("show databases")

for database in cursor.fetchall():
    print(database)
#cursor.execute("CREATE DATABASE BestOrder")

cursor.execute("CREATE TABLE tasks(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), task_description VARCHAR(11), priority INTEGER (11),list INTEGER (11), assignee INTEGER (11), Status VARCHAR (255))git")
cursor.execute("CREATE TABLE Lists(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR (255), list_description VARCHAR(255))")
cursor.execute("CREATE TABLE Assignees(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR (255), Total_tasks INTEGER(11), done_tasks INTEGER (11), undone_tasks INTEGER (11))")
