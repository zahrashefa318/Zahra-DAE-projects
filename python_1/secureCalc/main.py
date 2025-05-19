from flask import render_template
from prjctPackage import flaskApp
app=flaskApp()
@app.route('/')
def basePage():
    return render_template('base.html')
if __name__ =="__main__":
    app.run(debug=True)