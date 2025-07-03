original_list = [7, 2, 9, 4, 1, 8, 5, 10, 3, 6]
sortedList=[]


def make_sorted_copy(original_list):
    original_list_copy=original_list
    
    while len(original_list_copy) > 0:
        sortedList.append(min(original_list_copy))
        original_list_copy.remove(min(original_list_copy))
        

    return sortedList
print(original_list)
print(make_sorted_copy(original_list))