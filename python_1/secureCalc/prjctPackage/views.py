from flask import Blueprint , request, render_template , jsonify, url_for, redirect,flash ,session
from .SimpleArithmetic import SimpleArithmetic
from .utils import nocache


views=Blueprint('views', __name__)
arithmeticFnc=SimpleArithmetic()

@views.route('/multiplactionTable', methods=['GET','POST'])
@nocache
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
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('authRouts.loginHome'))
    elif request.method == 'POST':
        try:
            number=request.form.get('numberInput')
            htmlTbleResult=arithmeticFnc.multiplactionTable(number)
            return render_template('result.html', resultTable=htmlTbleResult , number=number)
        except ValueError as e:
            flash(f"Invalid input: {e}", 'danger')
            return redirect(url_for('views.multiplactionTable'))
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", 'danger')
            return redirect(url_for('views.multiplactionTable'))
        

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
    if request.method == 'POST':
        try:
            data = request.get_json()
            numbers = data.get('numbers', [])
            print(numbers)
            
            total =arithmeticFnc.summation(numbers)
            print(total)
            return jsonify({'total': total})

        except TypeError as e:
            flash(f"Invalid data format: {e}", 'danger')
            return redirect(url_for('views.result'))
            
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", 'danger')
            return redirect(url_for('views.result')) 
            
    

@views.route('/result' ,methods=['GET'])
@nocache
def result():
    """
    Display the result page with the calculated total.

    This route is protected and requires the user to be logged in.
    If the user is not logged in, they are redirected to the login page.
    The route retrieves the 'total' value from the query parameters
    and renders the 'result.html' template with that value.

    Returns:
        Rendered HTML template for the result page or redirect to login.
    """
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('authRouts.loginHome'))
    total = request.args.get('total', type=float)
    if total == None:
        flash("Error!!!!","danger")
        
    print(f"hi this is :{total}")
    return render_template('result.html', total=total)
    


@views.route('/getPrecentage' , methods=['GET','POST'])
@nocache
def getPrecentage():
    """
    Handle percentage calculation requests and display results.

    - Requires the user to be logged in. If not authenticated, redirects to login.
    - On GET request: renders the form for percentage calculation.
    - On POST request:
        - Retrieves 'input1' as the percentage and 'input2' as the base value.
        - Calls the arithmeticFnc.precentageCalculator() function to compute the result.
        - Renders the 'result.html' template with the computed result.
        - If input is invalid or an exception occurs, displays an error and redirects.

    Returns:
        Rendered HTML form or result page, or redirect with error message.
    """
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('authRouts.loginHome'))
    elif request.method == 'POST':
        try:
            precentage=request.form.get('input1')
            baseValue=request.form.get('input2')
            result=arithmeticFnc.precentageCalculator(precentage, baseValue)
            return render_template('result.html', precentageResult=result , precentage=precentage , baseValue=baseValue)
        except ValueError as e:
            flash(f"Invalid input: {e}", 'danger')
            return redirect(url_for('views.getPrecentage'))
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", 'danger')
            return redirect(url_for('views.getPrecentage'))
    return render_template('result.html')    

@views.route('/getAverage', methods=['POST'])
def getAverage():
     """
    Calculate the average of a list of numbers sent via a JSON POST request.

    - Expects a JSON payload with a 'numbers' key containing a list of numbers.
    - Calls arithmeticFnc.averageCalculator() to compute the average.
    - Returns a JSON response with the calculated average.
    - If the input is not properly formatted or another error occurs,
      flashes an error message and redirects to the number input page.

    Returns:
        JSON response with the average, or redirect with an error message.
    """

     if request.method == 'POST':
        try:
            data = request.get_json()
            numbers = data.get('numbers', [])
            average=arithmeticFnc.averageCalculator(numbers)
            return jsonify({'average': average})
        except TypeError as e:
            flash(f"Invalid data format: {e}", 'danger')
            return redirect(url_for('views.gettingNumbers'))
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", 'danger')
            return redirect(url_for('views.gettingNumbers'))


@views.route('/averageResult' , methods=['GET'])
@nocache
def avrageResult():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('authRouts.loginHome'))
    average = request.args.get('average', type=float)
    return render_template('result.html', average=average)


@views.route('/remainder', methods=['GET','POST'])
@nocache
def remainder ():
     """
    Handle requests to compute the remainder of two numbers.

    This route supports both GET and POST methods. For GET requests, it renders
    the input form for users to enter the dividend and divisor. For POST requests,
    it processes the form data to compute the remainder.

    - If the user is not authenticated (i.e., 'user_id' not in session), they are
      redirected to the login page with a warning message.
    - If the divisor is zero, a warning message is flashed, and the user is
      redirected to the dashboard.
    - If the inputs are valid, the remainder is calculated using
      `arithmeticFnc.remainderCalculator`, and the result is displayed on the
      'result.html' template.
    - Handles ValueError and general exceptions by flashing appropriate error
      messages and redirecting the user accordingly.

    Returns:
        Response: Renders a template or redirects to another route based on the
        request method and input validation.
    """
    
     if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('authRouts.loginHome'))
     elif request.method == 'POST':
        try:
            number=request.form.get('input1')
            divisor=request.form.get('input2')
            if divisor == '0':
                flash("Not zero divisor allowed!","warning")
                return redirect(url_for('authRouts.dashboard'))
            else:
                result=arithmeticFnc.remainderCalculator(number, divisor)
                print(result)
                return render_template('result.html', number=number ,divisor= divisor ,remainder= result)
        except ValueError as e:
            flash(f"Invalid input: {e}", 'danger')
            return redirect(url_for('authRouts.dashboard'))
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", 'danger')
            return redirect(url_for('views.remainder'))
        

@views.route('/gettingNumbersForMinMax' , methods=['POST'])
def gettingNumbersForMinMax():
     """
    Process a POST request to compute the minimum and maximum values from a list of numbers.

    Expects a JSON payload with a 'numbers' key containing a list of numerical values. Calculates
    the minimum and maximum using the `arithmeticFnc.minMaxCalculator` function.

    Returns:
        Response: A JSON response containing 'minValue' and 'maxValue' keys with their respective
        computed values.

    Error Handling:
        - If the input data is not in the expected format (e.g., 'numbers' is not a list), a
          TypeError is caught, a flash message is displayed, and the user is redirected to the
          'gettingNumbers' page.
        - For any other exceptions, a generic error message is flashed, and the user is redirected
          to the 'gettingNumbers' page.
    """

     if request.method == 'POST':
        try:
            data=request.get_json()
            numbers=data.get('numbers',[])
            minValue , maxValue=arithmeticFnc.minMaxCalculator(numbers)
            print(minValue , maxValue)
            return jsonify({'minValue':minValue ,'maxValue':maxValue})
        except TypeError as e:
            flash(f"Invalid data format: {e}", 'danger')
            return redirect(url_for('views.minMaxResult'))
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", 'danger')
            return redirect(url_for('views.minMaxxResult'))

        

@views.route('/minMaxResult',methods=['GET'])
@nocache
def minMaxResult():
  """
    Render the result page displaying the minimum and maximum values.

    Retrieves 'minValue' and 'maxValue' from the query parameters. If the user is not authenticated
    (i.e., 'user_id' not in session), they are redirected to the login page with a warning message.

    Returns:
        Response: Renders the 'result.html' template with 'minValue' and 'maxValue' passed as
        context variables.

    Notes:
        - Default values are used if 'minValue' or 'maxValue' are not provided in the query
          parameters: 0 for 'minValue' and 100 for 'maxValue'.
    """

  if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('authRouts.loginHome'))
  minv=request.args.get('minValue', default=0,type=int)
  maxv=request.args.get('maxValue' ,default=100, type=int)
  return render_template('result.html',minValue=minv , maxValue=maxv)


 
    