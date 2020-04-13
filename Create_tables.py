import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")

cursor = db.cursor()

cursor.execute("show tables")

for table in cursor.fetchall():
    print(table)
#cursor.execute("CREATE DATABASE BestOrder")
cursor.execute("DROP TABLE assignees")
cursor.execute("DROP TABLE tasks")
cursor.execute("DROP TABLE Lists")
cursor.execute("CREATE TABLE tasks(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), task_description VARCHAR(255), priority INTEGER(11),list INTEGER(11), assignee VARCHAR(255), status VARCHAR(255))")
cursor.execute("CREATE TABLE Lists(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR (255), list_description VARCHAR(255))")
cursor.execute("CREATE TABLE Assignees(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR (255), username VARCHAR(255) UNIQUE)")
#cursor.execute("ALTER TABLE Assignees DROP COLUMN Total_tasks")
#cursor.execute("ALTER TABLE Assignees DROP COLUMN done_tasks")
#cursor.execute(("ALTER TABLE Assignee MODIFY COLUMN undone task ADD UNIQUE username"))
#cursor.execute("DROP TABLE assignees")
#cursor.execute("ALTER TABLE tasks MODIFY COLUMN assignee VARCHAR(255)")
db.commit()