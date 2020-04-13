import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")

cursor = db.cursor()




class Task():

    def __init__(self, name, description, priority, list, assignee, status):
        self.name = name
        self.description = description
        self.priority = priority
        self.list = list
        self.assignee = assignee
        self.status = status

    def upload(self):
        new_task = [self.name, self.description, self.priority, self.list, self.assignee, self.status]
        cursor.execute("INSERT INTO tasks (name,task_description,priority,list,assignee,status) VALUES (%s, %s, %s, %s, %s, %s)",new_task)
        db.commit()

        print("successfully added a task")
        return "Seccessfully added a new task"

    def edit_task(self,id,name, description,priority, list, assignee,status):
        info_list=(name,description,priority,list,assignee,status,id)
        cursor.execute("UPDATE tasks SET name = %s, description = %s,priority = %s,list = %s,assignee = %s,status = %s WHERE id =%s",(info_list,))
        db.commit()

    def delete(self,id):
        self.id= id
        cursor.execute("DELETE FROM tasks WHERE id = %s",(id))
        db.commit()
        return "Success"



class List():

    def __init__(self,name,description):
        self.name = name
        self.description = description


    def upload(self):
        new_list = [self.name,self.description]
        cursor.execute("INSERT INTO lists (name,list_description) VALUES (%s,%s)", new_list)
        db.commit()


class Assignee():

    def __init__(self,name,username):
        self.name = name
        self.username = username

    def upload(self):
        assignee = (self.name,self.username)
        cursor.execute("INSERT INTO assignees (name,username) VALUES (%s,%s)", (assignee))
        db.commit()





def edit_task(column,new_info,id):
    info_list = [column,new_info,id]
    cursor.execute("UPDATE TABLE tasks SET (%s) = (%s) WHERE id = (%s)",info_list)
    db.commit()
    return "Success"

#edit_item("name",1,"attempt2","taks")