"""
    The program expects a python list in a textfile as input.
    Avg. runtime of Bubblesort: O(n²)
"""

import ast

numbers = input()
numbers = ast.literal_eval(numbers)
numbers = [int(i) for i in numbers]

for j in range(len(numbers)-1):
    for k in range(len(numbers)-1-j):
        if (numbers[k] > numbers[k+1]):
            tmp = numbers[k]
            numbers[k] = numbers[k+1]
            numbers[k+1] = tmp

print(numbers)