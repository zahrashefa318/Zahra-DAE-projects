from flask import Blueprint , request, render_template
from .import simpleArithmetic

views=Blueprint('views', __name__)

@views.route('/multiplactionTable', methods=['GET','POST'])
def multiplactionTable():
    if request.method == 'POST':
        number=request.form.get('numberInput')
        result=simpleArithmetic(number)
        return render_template('result.html', resultTable=result)
