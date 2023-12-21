"""
    The program expects a python list in a textfile as input.
    Avg. runtime of Selectionsort: O(n²)
"""

import ast

numbers = input()
numbers = ast.literal_eval(numbers)
numbers = [int(i) for i in numbers]

for j in range(len(numbers)-1):
    minIndex = j
    for k in range(j+1, len(numbers)):
        if (numbers[k] < numbers[minIndex]):
                    minIndex = k
    tmp = numbers[j]
    numbers[j] = numbers[minIndex]
    numbers[minIndex] = tmp

print(numbers)