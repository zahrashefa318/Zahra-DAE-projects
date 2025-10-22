from flask import Blueprint , render_template , request, redirect,url_for, flash,session
from .dbExtension import db
from .models import userInfo
from werkzeug.security import check_password_hash, generate_password_hash
from .utils import nocache
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from datetime import datetime

authRouts=Blueprint('authRouts', __name__ )

#*************The sign up routes and functions ****************

@authRouts.route('/signup')
def signup():
     """
    Handles the '/signup' route within the 'authRouts' Blueprint.

    This view function renders the 'signUp.html' template, which presents
    the user with a registration form to create a new account.

    Returns:
        A rendered HTML template displaying the signup form.
    """
     return render_template("signUp.html")

@authRouts.route('/register' , methods=['GET', 'POST'])
def register():
  """
    Handles user registration via the '/register' route.

    This view function supports both GET and POST HTTP methods:

    - GET: Renders the 'signUp.html' template, displaying the user registration form.
    - POST: Processes the submitted registration form data to create a new user account.

    The registration process includes:
    - Retrieving form data: 'name', 'lastname', 'email', 'password', and 'confirm'.
    - Validating that the 'password' and 'confirm' fields match.
    - Checking if a user with the provided email already exists in the database.
    - Hashing the password for secure storage.
    - Creating a new user record and committing it to the database.

    Error Handling:
    - If the passwords do not match, flashes an error message and redirects back to the signup page.
    - If the email already exists, flashes an error message and redirects back to the signup page.
    - Catches SQLAlchemy errors, rolls back the session, flashes a database error message, and redirects back to the signup page.
    - Catches any other exceptions, logs the error with a timestamp to 'app.log', flashes a generic error message, and redirects back to the signup page.

    Logging:
    - Logs an informational message indicating that the register route was accessed.

    Returns:
        - On GET: Rendered 'signUp.html' template.
        - On successful POST: Redirect to the login page.
        - On error during POST: Redirect back to the signup page with an appropriate flash message.
    """

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
                return redirect(url_for('authRouts.loginHome'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("A database error occurred. Please try again later.", "danger")
            return redirect(url_for('authRouts.signup'))

        except Exception as e:
            db.session.rollback()
            with open("app.log", "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {e}\n")
            flash("An unexpected error occurred. Please try again later.", "danger")
            return redirect(url_for('authRouts.signup'))

        finally:
            current_app.logger.info("Register route was accessed.")

  return render_template("signUp.html")
        

    

#***********The Log in routes and functions ******************

@authRouts.route('/loginHome',methods=['GET','POST'])
@nocache
def loginHome():
    """
    Handles user authentication via the '/loginHome' route.

    This view function supports both GET and POST HTTP methods:

    - GET: Renders the 'base.html' template, displaying the login form to the user.
    - POST: Processes the submitted login form data to authenticate the user.

    The authentication process includes:
    - Retrieving form data: 'email' and 'password'.
    - Querying the database for a user with the provided email.
    - Verifying the provided password against the stored hashed password.
    - If authentication is successful:
        - Stores the user's ID and name in the session.
        - Redirects the user to the dashboard.
    - If authentication fails:
        - Flashes an error message indicating invalid credentials.
        - Redirects back to the login page.

    Error Handling:
    - Catches SQLAlchemy errors, flashes a database error message, and redirects back to the login page.
    - Catches any other exceptions, flashes a generic error message, and redirects back to the login page.

    Logging:
    - Logs an informational message indicating that the loginHome route was accessed.

    Returns:
        - On GET: Rendered 'base.html' template.
        - On successful POST: Redirect to the dashboard.
        - On error during POST: Redirect back to the login page with an appropriate flash message.
    """
    
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
       finally:
            # This block executes regardless of exceptions
            current_app.logger.info("loginHome route was accessed.")
       

    return render_template('base.html')

@authRouts.route('/dashboard')
@nocache
def dashboard():
    """
    Renders the user's dashboard page upon successful authentication.

    This view function performs the following operations:
    - Checks if the user is authenticated by verifying the presence of 'user_id' in the session.
    - If the user is not authenticated:
        - Flashes a warning message prompting the user to log in.
        - Redirects the user to the login page.
    - If the user is authenticated:
        - Renders the 'home.html' template, passing the user's name from the session for personalized display.

    Returns:
        - On unauthenticated access: Redirects to the login page with a flash message.
        - On authenticated access: Rendered 'home.html' template with the user's name.
    """
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('authRouts.loginHome'))
    return render_template('home.html', name=session['user_name'])


      

#*********** logout route and function ************************

@authRouts.route('/logout' , methods=['POST','GET'])
def logout():
    """
    Logs out the current user by clearing session data and redirecting to the base page.

    This route handles both GET and POST requests to log out the user. It performs the following actions:
    - Removes 'user_id' and 'user_name' from the session.
    - Clears the entire session to remove any remaining data.
    - Flashes a success message indicating the user has been logged out.
    - Redirects the user to the base page.

    In case of an exception during the logout process:
    - Flashes an error message.
    - Redirects the user back to the dashboard.

    Regardless of the outcome, logs an informational message indicating that the logout route was accessed.

    Returns:
        A redirect response to the appropriate page based on the outcome.
    """

    try:
        session.pop('user_id',None)
        session.pop('user_name', None)
        session.clear()
        flash("You have been logged out !", "success")
        return redirect(url_for('basePage'))
    except Exception as e:
        flash("An error occurred during logout. Please try again.", "danger")
        return redirect(url_for('authRouts.dashboard'))
    finally:
            # This block executes regardless of exceptions
            current_app.logger.info("logout route was accessed.")

       
       


       