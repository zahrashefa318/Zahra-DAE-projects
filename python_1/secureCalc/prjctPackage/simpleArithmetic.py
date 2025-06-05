import pandas as pd
class SimpleArithmetic :
    def __init__(self):
        pass

    def multiplactionTable(self, number):
        """
        Generates an HTML-formatted multiplication table for a given number.

        This method performs the following operations:
        - Converts the input 'number' to an integer and assigns it to 'self.number'.
        - Iterates from 1 to 20, creating a list of tuples containing:
            - The multiplier (1 through 20)
            - The original number
            - The product of the multiplier and the number
        - Constructs a pandas DataFrame from the list with columns: 'Multiplier', 'Number', and 'Result'.
        - Converts the DataFrame to an HTML table string with Bootstrap classes for styling.

        Parameters:
            number (int or str): The number for which to generate the multiplication table.

        Returns:
            str: An HTML string representing the multiplication table with Bootstrap styling.
        """
        self.number=int(number)
        multiplactionList=[]
        i = 1
        while i <= 20:
             multiplactionList.append((i, self.number, self.number * i))
             i += 1
        resultPandasTbl=pd.DataFrame(multiplactionList,columns=['Multiplier','Number','Result'])
        resultPdTohtmlTble=resultPandasTbl.to_html(classes='table table-bordered', index=False)
        return resultPdTohtmlTble    

    def summation(self, numberList):
        """
        Calculates the sum of a list of numbers with precision up to two decimal places.

        This method performs the following operations:
        - Assigns the input list to an instance variable 'self.list'.
        - Initializes a 'total' variable to 0.
        - Iterates through each number in 'self.list':
            - Adds the number to 'total'.
            - Rounds 'total' to two decimal places after each addition.
        - Returns the final 'total' as the sum of the numbers, rounded to two decimal places.

        Parameters:
            numberList (list of float): A list containing numerical values to be summed.

        Returns:
            float: The sum of the numbers in 'numberList', rounded to two decimal places.
        """
        
        self.list=numberList
        total=0
        for num in self.list:
            total +=num
            total=round(total , 2)
        return total    
    
    def precentageCalculator(self, precentage, baseValue):
        """
    Calculates the specified percentage of a base value.

    This method performs the following operations:
    - Converts the input 'percentage' and 'baseValue' to floats.
    - Computes the result by multiplying the base value by the percentage divided by 100.
    - Rounds the result to two decimal places for precision.

    Parameters:
        percentage (float or str): The percentage to calculate.
        baseValue (float or str): The base value on which the percentage is calculated.

    Returns:
        float: The result of the percentage calculation, rounded to two decimal places.

    Example:
        >>> percentageCalculator(15, 200)
        30.0
    """
        self.precentage=float(precentage)
        self. baseValue=float(baseValue)
        result=(self.precentage / 100)*self.baseValue
        result=round(result ,2)
        return result
    

    def averageCalculator(self, numbers):
        """
        Calculates the average (arithmetic mean) of a list of numerical values.

        This method performs the following operations:
        - Assigns the input list to an instance variable 'self.numbers'.
        - Calculates the total sum of the numbers using the 'summation' method.
        - Divides the total by the number of elements to compute the average.
        - Rounds the average to two decimal places for precision.

        Parameters:
            numbers (list of float): A list containing numerical values.

        Returns:
            float: The average of the numbers in the list, rounded to two decimal places.

        Raises:
            ValueError: If the input list is empty.

        Example:
            >>> averageCalculator([10, 20, 30])
            20.0
        """

        self.numbers=numbers
        total =self.summation(numbers)
        average=total/len(numbers)
        average=round(average , 2)
        return average
        
    def remainderCalculator(self , number , divisor):
        """
        Calculates the remainder of the division of two numbers.

        This method performs the following operations:
        - Converts the input 'number' and 'divisor' to floats.
        - Computes the remainder by dividing 'number' by 'divisor'.
        - Rounds the result to two decimal places for precision.

        Parameters:
            number (float or str): The number to be divided.
            divisor (float or str): The number by which 'number' is divided.

        Returns:
            float: The remainder of the division, rounded to two decimal places.

        Raises:
            ValueError: If the input 'number' or 'divisor' cannot be converted to floats.
            ZeroDivisionError: If 'divisor' is zero.

        Example:
            >>> remainderCalculator(10, 3)
            1.0
        """
        self.number=float(number)
        self.divisor=float(divisor)
        result=self.number % self.divisor
        result=round(result , 2)
        return result
    
    def minMaxCalculator(self, numbers):
        """
        Calculates the minimum and maximum values from a list of numbers.

        This method performs the following operations:
        - Converts the input 'numbers' to a list of floats.
        - Computes the minimum and maximum values from the list.

        Parameters:
            numbers (iterable): A sequence of numerical values (e.g., list, tuple).

        Returns:
            tuple: A tuple containing the minimum and maximum values.

        Raises:
            ValueError: If the input 'numbers' cannot be converted to floats.

        Example:
            >>> minMaxCalculator([1, 2, 3, 4, 5])
            (1.0, 5.0)
        """
        self.numbers= list(map(float , numbers))
        minValue=min(self.numbers)
        maxValue=max(self.numbers)
        return minValue , maxValue