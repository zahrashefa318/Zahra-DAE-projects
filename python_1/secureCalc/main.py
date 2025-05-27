from flask import render_template
from prjctPackage import flaskApp
app=flaskApp()
@app.route('/')
def basePage():
    """Renders the base HTML page of the application.

    This route serves the main entry point of the application, displaying
    the base template (`base.html`) to the user. It is typically used as
    the landing page or home page of the web application.


    Returns:
         Response: The rendered HTML content of the base page.
    """
    return render_template('base.html')
if __name__ =="__main__":
    app.run(debug=True)