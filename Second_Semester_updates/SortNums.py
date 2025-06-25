original_list = [7, 2, 9, 4, 1, 8, 5, 10, 3, 6]
sortedList=[]


def make_sorted_copy(original_list):
    i=1
    for num in range(1,11):
        if num < original_list[i]:
            sortedList.append(num)
            i=+1
         

    return sortedList

print(make_sorted_copy(original_list))