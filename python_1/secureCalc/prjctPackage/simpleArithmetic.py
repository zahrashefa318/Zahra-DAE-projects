class SimpleArithmetic :
    def __init__(self):
        pass

    def multiplactionTable(self, number):
        self.number=number
        for i in range(1,11):
            print(f'{i}*{self.number}={i*self.number}')

    def summation(self, numberList):
        self.list=numberList
        total=0
        
        for num in self.list:
            total +=num
        return total    
