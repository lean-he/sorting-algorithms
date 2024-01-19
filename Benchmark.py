import argparse
import ast
from datetime import datetime
import matplotlib.pyplot as plt
import os
import random
import subprocess
import time
from tqdm import tqdm

queue = [("c", "Bubblesort"), ("java", "Bubblesort.class"), ("python", "Bubblesort.py"),
        ("c", "Quicksort"), ("java", "Quicksort.class"), ("python", "Quicksort.py"),
        ("c", "Selectionsort"), ("java", "Selectionsort.class"), ("python", "Selectionsort.py",)]

bubblesort = {"c": [], "java": [], "python": []}
quicksort = {"c": [], "java": [], "python": []}
selectionsort = {"c": [], "java": [], "python": []}

def compile_code(file_name):
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
        subprocess.run(["java", "-cp", "build/java", file_name], input=input, capture_output=True, text=True)
    elif (file_name.endswith(".py")):
        subprocess.run(["python", "src/python/" + file_name], input=input, capture_output=True, text=True)
    else:
        subprocess.run(["build/c/" + file_name], input=input, capture_output=True, text=True)

def measure_real_time(file_names, input):
    start_time = time.time()
    run_code(file_names, input)
    end_time = time.time()
    return end_time - start_time

def make_result_plot(results, n):
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
    plt.savefig("result_last.png")
    plt.savefig("results/result_" + str(datetime.today().strftime("%Y-%m-%d_%H.%M.%S")) + ".png")
    plt.close()

def main():
    parser = argparse.ArgumentParser(
        description="Bechmarking tool of sorting algorithms that creates presentable plots.")
    parser.add_argument("--recompile", action="store_true",
                        help="in case your executable sorting algorithm files are broken or missing.")
    parser.add_argument("--no-number-gen", action="store_true",
                        help="no generation of a new data set. The last used one will be used again. On the first execution is a generation however necessary.")
    parser.add_argument("-n", type=int, required=False, default=10000, help="N specifies the size of random elements that get sorted. The default value is 10000.")
    args = parser.parse_args()

    os.makedirs("build/c", exist_ok=True)
    os.makedirs("build/java", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    if (not os.listdir("build/c") or not os.listdir("build/java") or args.recompile):
        print("Initial start. Compiling needed files...")
        for i in os.listdir("src/c") + os.listdir("src/java"):
            compile_code(i)

    if (not args.no_number_gen):
        numbers = generate_data(args.n)
        f = open("data/numbers.txt", "w")
        f.write(str(numbers))
        f.close()
    else:
        f = open("data/numbers.txt", "r")
        numbers = ast.literal_eval(f.read())
        print(numbers)
        print(type(numbers))
        print(len(numbers))
        f.close()
        args.n = len(numbers)

    for i in tqdm((queue), desc="Total"):
        if "Bubblesort" in i[1]:
            bubblesort[i[0]].append(measure_real_time(i[1], str(numbers)))
        elif "Quicksort" in i[1]:
            quicksort[i[0]].append(measure_real_time(i[1], str(numbers)))
        elif "Selectionsort" in i[1]:
            selectionsort[i[0]].append(measure_real_time(i[1], str(numbers)))

    results = (bubblesort["c"] + bubblesort["java"] + bubblesort["python"] +
               quicksort["c"] + quicksort["java"] + quicksort["python"] +
               selectionsort["c"] + selectionsort["java"] + selectionsort["python"])

    make_result_plot(results, args.n)
    print("Done. A benchmark plot was saved in the program directory.")

if __name__ == "__main__":
    main()