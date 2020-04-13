from flask import Flask, render_template, request
import mysql.connector
from calsses import Classes
app = Flask(__name__)
db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")

cursor = db.cursor()

#cursor.execute("show databases")

#cursor.execute("show tables")


@app.route("/bestorder")
def show_main():
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    list_due_list = []
    task_list = []
    cursor.execute("SELECT * FROM lists")
    for list in cursor.fetchall():
        task_list.append(list)
    if len(task_list) > 0:
        cursor.execute("SELECT * FROM lists")
        for list in cursor.fetchall():
            list_id = list[0]
            list_name = list[1]
            list_due = (list[0], list[1])
            list_due_list.append(list_due)
        return render_template("main.html", Lists=list_due_list, list_id=list_id, list_name=list_name)
    return render_template("main.html")

@app.route("/list/<list_id>", methods=["GET"])
def show_list(list_id):
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    list_id=list_id
    cursor.execute("SELECT name,list_description FROM lists WHERE id = %s", (list_id,))
    for name, description in cursor.fetchall():
        list_name = name
        list_description = description
    cursor.execute("SELECT * FROM tasks WHERE list = %s", (list_id,))
    if len(cursor.fetchall()) > 0:
        cursor.execute("SELECT * FROM tasks WHERE list = %s", (list_id,))
        task_list = []
        for task in cursor.fetchall():
            task_id = task[0]
            task_name = task[1]
            task_priority = task[3]
            task_assignee = task[5]
            task_status = task[6]
            task_list_tuple = (task_id, task_name, task_priority, task_assignee, task_status)
            task_list.append(task_list_tuple)
        return render_template("list.html", list_name=list_name, list_description= list_description, tasks=task_list, list_id=list_id,
                               task_id=task_id, task_name=task_name,task_assignee=task_assignee, task_priority=task_priority, task_status=task_status)
    return render_template("list.html", list_name=list_name, list_description= list_description,list_id=list_id)
@app.route("/list/<list_id>", methods=["POST"])
def show_sort(list_id):
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    list_id=list_id
    yuval_order = request.form["sort"]
    cursor.execute("SELECT name,list_description FROM lists WHERE id = %s", (list_id,))
    for name, description in cursor.fetchall():
        list_name = name
        list_description = description
    #cursor.execute("SELECT * FROM tasks WHERE list = %s", (list_id,))
    #if len(cursor.fetchall()) > 0:
        task_list = []
    cursor.execute("SELECT * FROM tasks WHERE list = {} ORDER BY {}".format(list_id,yuval_order))
    for task in cursor.fetchall():
        task_id = task[0]
        task_name = task[1]
        task_priority = task[3]
        task_assignee = task[5]
        task_status = task[6]
        task_list_tuple = (task_id, task_name, task_priority, task_assignee, task_status)
        task_list.append(task_list_tuple)
    return render_template("list.html", list_name=list_name, list_description=list_description, tasks=task_list,
                   list_id=list_id,
                   task_id=task_id, task_name=task_name, task_assignee=task_assignee,
                   task_priority=task_priority, task_status=task_status)




@app.route("/all_tasks")
def show_all_tasks():
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    task_info_list=[]
    cursor.execute("SELECT * FROM tasks")
    if len(cursor.fetchall())>0:
        cursor.execute("SELECT * FROM tasks")
        for task in cursor.fetchall():
            task_id = task[0]
            task_name = task[1]
            task_priority = task[3]
            list_id = task[4]
            task_assignee = task [5]
            task_status = task[6]
            task_info=(task_id,task_name, task_priority, list_id, task_assignee, task_status)
            task_info_list.append(task_info)
        return render_template("Tasks.html", tasks = task_info_list, task=task_name, task_id=task_id,
                               task_priority=task_priority, task_list=list_id,task_assignee=task_assignee, task_status=task_status)
    return render_template("Tasks.html")

@app.route("/new_list", methods=["GET","POST"])
def new_task():
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    if request.method == "GET":
        return render_template("list_form.html")
    else :
        list_name = request.form["list_name"]
        list_description = request.form["list_description"]
        new_list = Classes.List(list_name, list_description)
        new_list.upload()
        message = "New list has been created :)"
        return render_template ("success.html", message=message)

@app.route("/task/<task_id>")
def show_task(task_id):
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    task_id = task_id
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    for task in cursor.fetchall():
        task_id = task[0]
        task_name = task[1]
        task_description = task[2]
        task_priority = task[3]
        task_list = task[4]
        task_assignee = task[5]
        task_status = task[6]
    return render_template("task.html", task_name=task_name, task_description=task_description, task_priority=task_priority, task_list=task_list, task_assignee=task_assignee, task_status= task_status,task_id=task_id)


@app.route("/<list_id>/new_task", methods=["GET","POST"])
def add_task(list_id):
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    assignee_list_final=[]
    cursor.execute("SELECT * FROM assignees")
    for name in cursor.fetchall():
        usernames = name[2]
        assignee_list_final.append(usernames)
    if request.method == "GET":
        return render_template("task_form.html", assignees=assignee_list_final)
    else :
        task_name = request.form["task_name"]
        task_description = request.form["task_description"]
        task_priority = request.form["task_priority"]
        task_list = list_id
        task_assignee = request.form["task_assignee"]
        task_status= request.form["task_status"]
        new_task = Classes.Task(task_name, task_description, task_priority, task_list, task_assignee, task_status)
        new_task.upload()
        message = "The New task has been added"
        return render_template ("success.html", message=message)

@app.route("/edit_task/<task_id>" ,methods=["GET","POST"])
def edit_task(task_id):
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    task_id=task_id
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    for task in cursor.fetchall():
        task_id = task[0]
        task_name = task[1]
        task_description = task[2]
        task_priority = task[3]
        task_list = task[4]
        task_assignee = task[5]
        task_status = task[6]
    assignee_list_final = []
    cursor.execute("SELECT * FROM assignees WHERE username = %s",(task_assignee,))
    for name in cursor.fetchall():
        usernames = name[2]
        if usernames == task_assignee:
            current_user = usernames
        assignee_list_final.append(current_user)
    for priority in range(6):
        if priority == task_priority:
            current_priority = priority
    if request.method == "GET":

        return render_template("edit_task.html", task_name=task_name, task_description=task_description, task_priority=task_priority,
                               task_list=task_list, current_user=task_assignee ,assignees=assignee_list_final, task_status= task_status,
                               username=current_user, task_id=task_id, current_priority=current_priority)
    else:
        task_name = request.form["task_name"]
        task_description = request.form["task_description"]
        task_priority = request.form["task_priority"]
        task_id = task_id
        task_assignee = request.form["task_assignee"]
        task_status = request.form["task_status"]
        info_list = [task_name, task_description, task_priority, task_assignee, task_status, task_id]
        cursor.execute("UPDATE tasks SET name = %s, task_description = %s,priority = %s,assignee = %s,status = %s WHERE id =%s",(info_list))
        db.commit()
        return render_template("success.html", message="You're Task has been successfully updated")

@app.route("/remove_task/<task_id>")
def remove_task(task_id):
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s",(task_id,))
    db.commit()
    message = "Your task has been removed :)"
    return render_template("success.html", message=message)

@app.route("/task_done/<task_id>")
def task_done(task_id):
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET Status = 'Done' WHERE id=%s",(task_id,))
    db.commit()
    message="Your task has been marked Done :) good job"
    return render_template("success.html", message=message)



@app.route("/all_assignees")
def show_assignees():
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    assignee_list=[]
    assignee_lists = []
    cursor.execute("SELECT name FROM assignees")
    #assignee_list.append(cursor.fetchall())
    if len(cursor.fetchall()) > 0:
        cursor.execute("SELECT * FROM assignees")
        for assignee in cursor.fetchall():
            assignee_id = assignee[0]
            assignee_name = assignee[1]
            username = assignee[2]
            assignee_tuple = (assignee_id,assignee_name,username)
            assignee_lists.append(assignee_tuple)
        return render_template("All_assignees.html", assignees=assignee_lists, assignee_name=assignee_name,assignee_id=assignee_id, username=username)
    return render_template("All_assignees.html")

@app.route("/new_assignee", methods=["GET","POST"])
def new_assignee():
    if request.method == "GET":
        return render_template("assignee_form.html")
    else :
        try :
            assignee_name = request.form["assignee_name"]
            assignee_username = request.form["assignee_username"]
            new_assignee = Classes.Assignee(assignee_name, assignee_username)
            new_assignee.upload()
            return render_template("success.html")
        except mysql.connector.errors.IntegrityError:
            return render_template("assignee_form.html", error="Username already taken")


@app.route("/assignee/<assignee_id>")
def show_assignee(assignee_id):
    db = mysql.connector.connect(host="localhost", user="root", password="toor", database="bestorder")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM assignees WHERE id = %s",(assignee_id,))
    for name in cursor.fetchall():
        assignee_name = name[1]
        username = name[2]
    task_list = []
    tasks_list = []
    cursor.execute("SELECT * FROM tasks WHERE assignee = %s", (username,))
    if len(cursor.fetchall()) > 0:
        cursor.execute("SELECT * FROM tasks WHERE assignee = %s", (username,))
        for task in cursor.fetchall():
            task_id = task[0]
            task_name = task[1]
            task_priority = task[3]
            task_list_id = task[4]
            task_status = task[6]
            task_list=(task_id,task_name,task_priority,task_list_id,task_status)

            tasks_list.append(task_list)
        return render_template("assignee.html", tasks=tasks_list, task_name=task_name, task_list=task_list_id,
                               task_id=task_list[0], task_priority=task_priority, task_status=task_status, assignee_name=assignee_name, username=username)
    return render_template("assignee.html", assignee_name=assignee_name, username=username)

if __name__== "__main__":
    app.run(host = "localhost", port = "9191", debug = True)