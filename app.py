from flask import Flask, request ,render_template , url_for , redirect, flash , g
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Configure APP(cors, database)
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    PhoneNumber = db.Column(db.String())
    Email = db.Column(db.String())

class Admin(db.Model):
    __tablename__ = 'Admin'
    Id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    
@app.route("/view-plan")
def view_plan():
    email =  request.args.get("email" , False)
    if email:
        return render_template("plan.html")
    else:
        return redirect(url_for('save_user'))
    

@app.route('/' , methods=["POST",'GET'])
def save_user():
    if request.method == "POST":
        email = request.form["email"]
        user = User(Name=request.form["name"], PhoneNumber=request.form["phone"], Email=request.form["email"])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('view_plan', email = email))

    if request.method == "GET":
        return render_template("base.html")


@app.route("/admin/view")
def userview():
    data = User.query.order_by(User.Id.desc())
    results = [
            {
                "Name": users.Name,
                "Email": users.Email,
                "Phone": users.PhoneNumber
            } for users in data]
    return render_template("userview.html" , data = results)

@app.route("/login" , methods = ["POST" ,"GET"])
def admin_login():
    if request.method == "POST":
        user = ""
        psw = ""
        adminData = Admin.query.all()
        result = [
                    {
                        "username": admin.username,
                        "password": admin.password,
                    } for admin in adminData
                ]
        for res in result:
            user = res['username']
            psw = res['password']
        if request.form['username'] == user and request.form['password'] == psw:
            return redirect(url_for('userview'))  
    return render_template('login.html')

@app.route("/logout")
def logout():
    return redirect(url_for('save_user'))

if __name__ == "__main__":
    print("Starting The Server....")
    app.debug = True
    app.run()