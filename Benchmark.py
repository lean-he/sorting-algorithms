import argparse
import ast
from cpuinfo import get_cpu_info
from datetime import datetime
import json
import matplotlib.pyplot as plt
import os
import random
import statistics
import subprocess
import time
from tqdm import tqdm

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

def run_code(file, input):
    if file[0] == "java":
        subprocess.run(["java", "-cp", "build/java", file[1]], input=input, capture_output=True, text=True)
    elif file[0] == "python":
        subprocess.run(["python", "src/python/" + file[1]], input=input, capture_output=True, text=True)
    elif file[0] == "c":
        subprocess.run(["build/c/" + file[1]], input=input, capture_output=True, text=True)

def measure_real_time(file, input):
    start_time = time.time()
    run_code(file, input)
    end_time = time.time()
    return end_time - start_time

def make_result_plot(result, n, k, timedate):
    names = ["C", "Java", "Python"]
    plt.figure(figsize=(15, 5))

    plt.subplot(131)
    bars = plt.bar(names, result[:3])
    plt.bar_label(bars)
    plt.ylabel("time (in seconds)")
    plt.title("Bubblesort")
    plt.subplot(132)
    bars = plt.bar(names, result[3:6])
    plt.bar_label(bars)
    plt.ylabel("time (in seconds)")
    plt.title("Quicksort")
    plt.subplot(133)
    bars = plt.bar(names, result[6:9])
    plt.bar_label(bars)
    plt.ylabel("time (in seconds)")
    plt.title("Selectionsort")

    if k > 1:
        plt.suptitle("Benchmark of sorting algorithms (" + str(n) + " elements in random order), (mean of " + str(k) + " runs)")
    else:
        plt.suptitle("Benchmark of sorting algorithms (" + str(n) + " elements in random order)")
    plt.savefig("result_last.png")
    plt.savefig("results/result_" + timedate + ".png")
    plt.close()

def write_result_to_file(result, timedate):
    with open("results/result_" + timedate + ".json", "w") as f:
        json.dump(result, f, indent=4)

def main():
    parser = argparse.ArgumentParser(
        description="Bechmarking tool of sorting algorithms that creates presentable plots.")
    parser.add_argument("--recompile", action="store_true",
                        help="in case your executable sorting algorithm files are broken or missing.")
    parser.add_argument("--no-number-gen", action="store_true",
                        help="no generation of a new data set. The last used one will be used again. On the first execution is a generation however necessary.")
    parser.add_argument("-n", type=int, required=False, default=5000, help="N specifies the size of random elements that get sorted. The default value is 5000.")
    parser.add_argument("-k", type=int, required=False, default=10, help="K specifies the number of algorithm runs. The default value is 10.")
    args = parser.parse_args()

    print("Getting CPU information...")

    queue = [("c", "Bubblesort"), ("java", "Bubblesort.class"), ("python", "Bubblesort.py"),
             ("c", "Quicksort"), ("java", "Quicksort.class"), ("python", "Quicksort.py"),
             ("c", "Selectionsort"), ("java", "Selectionsort.class"), ("python", "Selectionsort.py",)]

    result = {"algorithms": {"bubblesort": {"c": [], "java": [], "python": []},
                             "quicksort": {"c": [], "java": [], "python": []},
                             "selectionsort": {"c": [], "java": [], "python": []}},
              "cpuinfo": get_cpu_info()}
    
    init_timedate = str(datetime.today().strftime("%Y-%m-%d_%H.%M.%S"))

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

    print("Starting the algorithms...")

    for i in tqdm(range(1, args.k+1), desc="Total", colour="green", position=1):
        for j in tqdm(queue, desc="(" + str(i) + "/" + str(args.k) + ")", ascii=True, position=0):
            if "Bubblesort" in j[1]:
                result["algorithms"]["bubblesort"][j[0]].append(measure_real_time(j, str(numbers)))
            elif "Quicksort" in j[1]:
                result["algorithms"]["quicksort"][j[0]].append(measure_real_time(j, str(numbers)))
            elif "Selectionsort" in j[1]:
                result["algorithms"]["selectionsort"][j[0]].append(measure_real_time(j, str(numbers)))

    result_mean = ([statistics.mean(result["algorithms"]["bubblesort"]["c"])] +
                   [statistics.mean(result["algorithms"]["bubblesort"]["java"])] +
                   [statistics.mean(result["algorithms"]["bubblesort"]["python"])] +
                   [statistics.mean(result["algorithms"]["quicksort"]["c"])] +
                   [statistics.mean(result["algorithms"]["quicksort"]["java"])] +
                   [statistics.mean(result["algorithms"]["quicksort"]["python"])] +
                   [statistics.mean(result["algorithms"]["selectionsort"]["c"])] +
                   [statistics.mean(result["algorithms"]["selectionsort"]["java"])] +
                   [statistics.mean(result["algorithms"]["selectionsort"]["python"])])

    write_result_to_file(result, init_timedate)
    make_result_plot(result_mean, args.n, args.k, init_timedate)
    tqdm.write("Done. A benchmark plot was saved in the program directory.")

if __name__ == "__main__":
    main() 