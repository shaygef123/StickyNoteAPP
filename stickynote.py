from flask import Flask, request, render_template, redirect
from MongoDB import MongoDB,MongoACTION

DB_action = MongoACTION("root","A123a123",)
if not DB_action.is_DB_exists("StickyNote_Data"):
    DB_action.create_new_DB("StickyNote_Data","UsersDataBase")
else:
    if not DB_action.is_Collection_exists("StickyNote_Data","UsersDataBase"):
        DB_action.create_new_DB("StickyNote_Data", "UsersDataBase")

app = Flask(__name__)
mongo = MongoDB("root","A123a123","StickyNote_Data","UsersDataBase")

@app.route('/DB_status')
def status():
    return f"<center><h1>DataBase: {DB_action.is_DB_exists('StickyNote_Data')}\nCollection: {DB_action.is_Collection_exists('StickyNote_Data','UsersDataBase')}</h1></center>"

@app.route('/home', methods=["GET","POST"])
def home():
    if request.method == "POST":
        if request.form['submit_button'] == "login":
            global ID
            try:
                ID = int(request.form["ID"])
            except ValueError:
                return "ID must be number!"
            login = mongo.login_check(request.form["username"],ID,request.form["password"])
            print("login is:\n",login) # for test!!!
            if login :
                return redirect('/Mynote')
            elif login == None:
                return "Username does not exists"
            else:
                return "Authentication failed"

        elif request.form['submit_button'] == "Create new member":
            return redirect('/create')

    return render_template("Home.html")

@app.route('/create', methods=["GET","POST"])
def create_user():
    if request.method == "POST":
        if request.form['submit_button'] == "Back":
            return redirect('/home')

        elif request.form['submit_button'] == "Create":
            try:
                ID = int(request.form["ID"])
            except ValueError:
                return "ID must be number!"
            try:
                is_created = mongo.create_new_user(request.form["new_username"],ID,request.form["new_password"])
                if is_created:
                    return "The user created successfuly"
                else:
                    return is_created
            except:
                return "cannot create user"

    return render_template("Create_user.html")

@app.route('/Mynote', methods=["GET", "POST"])
def StickyNote():
    if request.method == "POST":
        if request.form['submit_button'] == "Back":
            return redirect('/home')
        if request.form['submit_button'] == "Save":
            new_data = request.form["edit_text"]
            resulte = mongo.edit_data(ID,new_data)
            if not resulte:
                return f"data updated with status {resulte}"
    return render_template("StickyNote.html", body=mongo.get_data(ID))

if __name__ == '__main__':
    app.run(debug=True,port=2999 ,host="0.0.0.0")