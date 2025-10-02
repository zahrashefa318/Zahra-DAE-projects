def show_total(numbers):
   total = 0
   for number in numbers:  # bug: wrong variable name
       total += number
   print("Total:", total)
show_total([1, 2, 3])
 