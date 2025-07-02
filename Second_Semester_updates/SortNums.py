original_list = [7, 2, 9, 4, 1, 8, 5, 10, 3, 6]
sortedList=[]


def make_sorted_copy(original_list):
    original_list_copy=original_list
    
    currentIndex=0
    nextIndex=1
    while nextIndex < 9:
        if original_list_copy[currentIndex]< original_list_copy[nextIndex]:
            sortedList.append(original_list_copy[currentIndex])
            original_list_copy.remove(original_list_copy[currentIndex])
            currentIndex += 1
            nextIndex +=1
         

    return sortedList

print(make_sorted_copy(original_list))