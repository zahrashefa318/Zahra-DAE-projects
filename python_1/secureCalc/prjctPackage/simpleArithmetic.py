import pandas as pd
class SimpleArithmetic :
    def __init__(self):
        pass

    def multiplactionTable(self, number):
        self.number=int(number)
        multiplactionList=[]
        for i in range(1,21):
            multiplactionList.append((i,self.number,self.number*i))
        resultPandasTbl=pd.DataFrame(multiplactionList,columns=['Multiplier','Number','Result'])
        resultPdTohtmlTble=resultPandasTbl.to_html(classes='table table-bordered', index=False)
        return resultPdTohtmlTble    

    def summation(self, numberList):
        self.list=numberList
        total=0
        
        for num in self.list:
            total +=num
        return total    
