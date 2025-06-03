from flask import Blueprint , render_template , request, redirect,url_for, flash,session
from .dbExtension import db
from .models import userInfo
from werkzeug.security import check_password_hash, generate_password_hash
from .utils import nocache
from sqlalchemy.exc import SQLAlchemyError

authRouts=Blueprint('authRouts', __name__ )

#*************The sign up routes and functions ****************

@authRouts.route('/signup')
def signup():
    return render_template("signUp.html")

@authRouts.route('/register' , methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
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

        except SQLAlchemyError as e:
            db.session.rollback()
            flash("A database error occurred. Please try again later.", "danger")
            return redirect(url_for('authRouts.signup'))

        except Exception as e:
            flash("An unexpected error occurred. Please try again later.", "danger")
            return redirect(url_for('authRouts.signup'))

    return render_template("signUp.html")
        

    

#***********The Log in routes and functions ******************

@authRouts.route('/loginHome',methods=['GET','POST'])
@nocache
def loginHome():
    if request.method=='POST':
       try:
            email=request.form.get('email')
            password=request.form.get('password')
            exsistingUser=userInfo.query.filter_by(email=email).first()
            if exsistingUser and check_password_hash(exsistingUser.password ,password):
                session['user_id']=exsistingUser.id
                session['user_name']=exsistingUser.name
                return redirect(url_for('authRouts.dashboard'))
                

            else:
                flash("Your email does not exist or your password is wrong!","danger")
                return redirect(url_for('authRouts.loginHome'))
        
       except SQLAlchemyError as e:
            flash("A database error occurred. Please try again later.", "danger")
            return redirect(url_for('authRouts.loginHome'))

       except Exception as e:
            flash("An unexpected error occurred. Please try again later.", "danger")
            return redirect(url_for('authRouts.loginHome'))

    return render_template('base.html')

@authRouts.route('/dashboard')
@nocache
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('authRouts.loginHome'))
    return render_template('home.html', name=session['user_name'])    

#*********** logout route and function ************************

@authRouts.route('/logout' , methods=['POST','GET'])
def logout():
    try:
        session.pop('user_id',None)
        session.pop('user_name', None)
        session.clear()
        flash("You have been logged out !", "success")
        return redirect(url_for('basePage'))
    except Exception as e:
        flash("An error occurred during logout. Please try again.", "danger")
        return redirect(url_for('authRouts.dashboard'))

       
       


       