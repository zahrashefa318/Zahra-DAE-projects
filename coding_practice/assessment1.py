mylist=[0,1,4,3,5,2,4]
def findFirstRepeated(theList):
   elemsInRange=len(theList)-1
   i=1
   for n in theList:
    
      for i in range(2,elemsInRange):
         if n == mylist[i]:
            print(n)
            return
         else:
            i +=1
            
findFirstRepeated(mylist)
         
