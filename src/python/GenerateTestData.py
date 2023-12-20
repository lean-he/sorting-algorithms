import random
import sys

n = int(sys.argv[1])
numbers = list(range(1, n+1))
random.shuffle(numbers)
print(numbers)
