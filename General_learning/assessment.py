text=input("Enter the text you want to revers:")

def reverse(input):
    revised=[]
    chrs=len(input)-1
    while chrs >= 0:
        revised.append(input[chrs])
        chrs -=1
    print(*revised,sep="")

reverse(text)
