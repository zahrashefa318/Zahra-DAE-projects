import pandas as pd
class SimpleArithmetic :
    def __init__(self):
        pass

    def multiplactionTable(self, number):
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
        self.list=numberList
        total=0
        for num in self.list:
            total +=num
            total=round(total , 2)
        return total    
    
    def precentageCalculator(self, precentage, baseValue):
        self.precentage=float(precentage)
        self. baseValue=float(baseValue)
        result=(self.precentage / 100)*self.baseValue
        result=round(result ,2)
        return result
    

    def averageCalculator(self, numbers):
        self.numbers=numbers
        total =self.summation(numbers)
        average=total/len(numbers)
        average=round(average , 2)
        return average
        
    def remainderCalculator(self , number , divisor):
        self.number=float(number)
        self.divisor=float(divisor)
        result=self.number % self.divisor
        result=round(result , 2)
        return result
    
    def minMaxCalculator(self, numbers):
        self.numbers= list(map(float , numbers))
        minValue=min(self.numbers)
        maxValue=max(self.numbers)
        return minValue , maxValue