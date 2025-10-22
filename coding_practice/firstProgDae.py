print("This is a program that evauates your  input number whether it is an odd or even!")
condition=True
num=0
try:
    while condition:
        num=int(input("Enter a valid , positive and integer number:"))
        if num > 0 :
            condition=False
            
            if num % 2 == 0:
                print("This is an even number.") 
            else :
                print("This is an odd number.")   

            more=input("Do you want to enter more numbers? y for 'yes' and n for 'no':")    
            more=more.lower()
            if more == "y":
                condition=True
            elif more =="n":
                condition=False
            else:
                print("Just enter y or n !")

except Exception :
    print("Enter a number please!")
