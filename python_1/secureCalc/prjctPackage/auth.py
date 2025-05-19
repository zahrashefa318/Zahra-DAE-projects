from flask import Blueprint , render_template , request, redirect,url_for, flash,session
from .dbExtension import db
from .models import userInfo
from werkzeug.security import check_password_hash, generate_password_hash

authRouts=Blueprint('authRouts', __name__ )

#*************The sign up routes and functions ****************

@authRouts.route('/signup')
def signup():
    return render_template("signUp.html")

@authRouts.route('/register' , methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name=request.form.get('name')
        lastname=request.form.get('lastname')
        email=request.form.get('email')
        password=request.form.get('password')
        confirm=request.form.get('confirm')
        hashed_password = generate_password_hash(password)
        exsistingUser=userInfo.query.filter_by(email=email).first()
        if password != confirm:
            flash("Password does not match!","danger")
            return redirect(url_for('authRouts.signup'))
        
        
        elif exsistingUser:
            flash("Your email already exist in database !","danger")
            return redirect(url_for('authRouts.signup'))
        else:

            newUser=userInfo(name=name,lastname=lastname,email=email,password=hashed_password)
            db.session.add(newUser)
            db.session.commit()
        
            return render_template('home.html', name=name, lastname=lastname)


        

    

#***********The Log in routes and functions ******************

@authRouts.route('/loginHome',methods=['GET','POST'])
def loginHome():
    if request.method=='POST':
       email=request.form.get('email')
       password=request.form.get('password')
       exsistingUser=userInfo.query.filter_by(email=email).first()
       if exsistingUser and check_password_hash(exsistingUser.password ,password):
           session['user_id']=exsistingUser.id
           session['user_name']=exsistingUser.name
           return render_template('home.html', name=exsistingUser.name , lastname=exsistingUser.lastname)
       else:
           flash("Your email does not exist or your password is wrong!","danger")
           return redirect(url_for('basePage'))
       
       


       