#! /bin/bash

mkdir build/c -p
mkdir build/python -p
mkdir data -p

python src/python/GenerateTestData.py 10000 > data/num10000.txt
python src/python/GenerateTestData.py 100000 > data/num100000.txt

gcc -o build/c/Bubblesort src/c/Bubblesort.c -O2 -Wno-unused-result
gcc -o build/c/Quicksort src/c/Quicksort.c -O2 -Wno-unused-result
gcc -o build/c/Selectionsort src/c/Selectionsort.c -O2 -Wno-unused-result

echo "Bubblesort (C) (10000 Elements)"
time build/c/Bubblesort < data/num10000.txt > data/out.txt
echo "Quicksort (C) (10000 Elements)"
time build/c/Quicksort < data/num10000.txt > data/out.txt
echo "Selectionsort (C) (10000 Elements)"
time build/c/Selectionsort < data/num10000.txt > data/out.txt