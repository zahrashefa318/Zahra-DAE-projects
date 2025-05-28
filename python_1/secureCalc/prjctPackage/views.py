from flask import Blueprint , request, render_template , jsonify, url_for, redirect
from .SimpleArithmetic import SimpleArithmetic

views=Blueprint('views', __name__)
arithmeticFnc=SimpleArithmetic()

@views.route('/multiplactionTable', methods=['GET','POST'])
def multiplactionTable():
    """Renders a multiplication table based on user input.

    This route handles both GET and POST requests. On a GET request, it renders
    the initial form for the user to input a number. On a POST request, it processes
    the submitted number, generates the multiplication table using the
    `multiplicationTable` function from the `arithmeticFnc` module, and renders
    the `result.html` template displaying the generated table.


    Returns:
        Response: The rendered HTML page displaying the multiplication table.
    """
    if request.method == 'POST':
        number=request.form.get('numberInput')
        htmlTbleResult=arithmeticFnc.multiplactionTable(number)
        return render_template('result.html', resultTable=htmlTbleResult , number=number)
    
@views.route('/gettingNumbers', methods=['POST','GET'])
def gettingNumbers():
    """
    Processes a POST request containing a JSON payload with a list of numbers,
    calculates their sum, and renders the result in an HTML template.

    This route expects a JSON object with a key 'numbers' containing a list of numeric values.
    It calculates the sum of these numbers and passes the result to the 'result.html' template
    for rendering.


    Returns:
         Response: The rendered HTML page displaying the calculated sum.
    """
    data = request.get_json()
    numbers = data.get('numbers', [])
    total =arithmeticFnc.summation(numbers)
    return jsonify({'total': total})


@views.route('/result' ,methods=['GET'])
def result():
    total = request.args.get('total', type=int)
    return render_template('result.html', total=total)

@views.route('/getPrecentage' , methods=['GET','POST'])
def getPrecentage():
    if request.method == 'POST':
        precentage=request.form.get('input1')
        baseValue=request.form.get('input2')
        result=arithmeticFnc.precentageCalculator(precentage, baseValue)
        return render_template('result.html', precentageResult=result , precentage=precentage , baseValue=baseValue)
    
@views.route('/getAverage', methods=['POST'])
def getAverage():
    data = request.get_json()
    numbers = data.get('numbers', [])
    average=arithmeticFnc.averageCalculator(numbers)
    return jsonify({'average': average})

@views.route('/averageResult' ,methods=['GET'])
def avrageResult():
    average = request.args.get('average', type=float)
    return render_template('result.html', average=average)