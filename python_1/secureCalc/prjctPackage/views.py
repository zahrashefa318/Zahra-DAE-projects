from flask import Blueprint , request, render_template
from .SimpleArithmetic import SimpleArithmetic

views=Blueprint('views', __name__)
arithmeticFnc=SimpleArithmetic()

@views.route('/multiplactionTable', methods=['GET','POST'])
def multiplactionTable():
    if request.method == 'POST':
        number=request.form.get('numberInput')
        htmlTbleResult=arithmeticFnc.multiplactionTable(number)
        return render_template('result.html', resultTable=htmlTbleResult , number=number)
