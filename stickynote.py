from flask import Flask, request, render_template, redirect
from MongoDB import MongoDB

app = Flask(__name__)
mongo = MongoDB("root","A123a123","StickyNote_Data","UsersDataBase")


@app.route('/home', methods=["GET","POST"])
def home():
    if request.method == "POST":
        if request.form['submit_button'] == "login":
            login = mongo.login_check(request.form["username"],request.form["ID"],request.form["password"])
            if login :
                global ID
                ID = request.form["ID"]
                return redirect('/Mynote')
            else:
                return "There is no username or your identification details is incorrect"

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
                is_created = mongo.create_new_user(request.form["new_username"],request.form["ID"],request.form["new_password"])
                if is_created == "True":
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