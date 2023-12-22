import matplotlib.pyplot as plt
import os
import random
import subprocess
import time

n = 10000

run_files = ["Bubblesort", "Bubblesort.class", "Bubblesort.py",
             "Quicksort", "Quicksort.class", "Quicksort.py",
             "Selectionsort", "Selectionsort.class", "Selectionsort.py"]

def compile_code(file_name):
    print("Compiling " + file_name + "...")
    if (file_name.endswith(".c")):
        subprocess.run(["gcc", "-o", "build/c/" + file_name.replace(".c", ""), "src/c/" + file_name, "-O2", "-Wno-unused-result"])
    elif (file_name.endswith(".java")):
        subprocess.run(["javac", "-d", "build/java", "src/java/" + file_name])

def generate_data(n):
    print("Generating list with " + str(n) + " elements in random order...")
    numbers = list(range(1, n+1))
    random.shuffle(numbers)
    return numbers

def run_code(file_name, input):
    if (file_name.endswith(".class")):
        print("Running " + file_name + " (Java)...")
        subprocess.run(["java", "-cp", "build/java", file_name], input=input, capture_output=True, text=True)
    elif (file_name.endswith(".py")):
        print("Running " + file_name + " (Python)...")
        subprocess.run(["python", "src/python/" + file_name], input=input, capture_output=True, text=True)
    else:
        print("Running " + file_name + " (C)...")
        subprocess.run(["build/c/" + file_name], input=input, capture_output=True, text=True)

def measure_real_time(file_names, input):
    start_time = time.time()
    run_code(file_names, input)
    end_time = time.time()
    return end_time - start_time

def make_result_plot(results):
    names = ["C", "Java", "Python"]
    plt.figure(figsize=(15, 5))

    plt.subplot(131)
    bars = plt.bar(names, results[:3])
    plt.bar_label(bars)
    plt.ylabel("time (in seconds)")
    plt.title("Bubblesort")
    plt.subplot(132)
    bars = plt.bar(names, results[3:6])
    plt.bar_label(bars)
    plt.ylabel("time (in seconds)")
    plt.title("Quicksort")
    plt.subplot(133)
    bars = plt.bar(names, results[6:9])
    plt.bar_label(bars)
    plt.ylabel("time (in seconds)")
    plt.title("Selectionsort")

    plt.suptitle("Benchmark of sorting algorithms (" + str(n) + " elements in random order)")
    plt.savefig("result.png")
    plt.close()

os.makedirs("build/c", exist_ok=True)
os.makedirs("build/java", exist_ok=True)
os.makedirs("data", exist_ok=True)

for i in os.listdir("src/c") + os.listdir("src/java"):
    compile_code(i)

numbers = generate_data(n)
f = open("data/numbers.txt", "w")
f.write(str(numbers))
f.close()

results = [measure_real_time(run_files[i], str(numbers)) for i in range(len(run_files))]

make_result_plot(results)
print("Done. A benchmark plot was saved in the program directory.")