import argparse
import ast
from cpuinfo import get_cpu_info
from datetime import datetime
import json
import matplotlib.pyplot as plt
import os
import random
from statistics import mean
import subprocess
import time
from tqdm import tqdm

def compile_code(file_name):
    if (file_name.endswith(".c")):
        subprocess.run(["gcc", "-o", "build/c/" + file_name.replace(".c", ""),
                        "src/c/" + file_name, "-O2", "-Wno-unused-result"])
    elif (file_name.endswith(".java")):
        subprocess.run(["javac", "-d", "build/java", "src/java/" + file_name])

def generate_data(n):
    print("Generating list with " + str(n) + " elements in random order...")
    numbers = list(range(1, n+1))
    random.shuffle(numbers)
    return numbers

def run_code(file, input):
    if file[0] == "Java":
        subprocess.run(["java", "-cp", "build/java", file[1]], input=input, 
                       capture_output=True, text=True)
    elif file[0] == "Python":
        subprocess.run(["python3", "src/python/" + file[1]], input=input, 
                       capture_output=True, text=True)
    elif file[0] == "C":
        subprocess.run(["build/c/" + file[1]], input=input, 
                       capture_output=True, text=True)

def measure_real_time(file, input):
    start_time = time.time()
    run_code(file, input)
    end_time = time.time()
    return end_time - start_time

def make_result_plot(result, n, k, timedate):
    algo_result = result["algorithms"]
    plt.figure(figsize=(len(algo_result)*5, len(algo_result)*1.6))
    if k > 1:
        plt.suptitle("Benchmark of sorting algorithms (" + str(n) +
                     " elements in random order), (mean of " + str(k) + " runs)")
    else:
        plt.suptitle("Benchmark of sorting algorithms (" + str(n) +
                     " elements in random order)")

    for i, algo in enumerate(algo_result):
        algo_languages = list(algo_result[algo].keys())
        algo_values = []

        for j in algo_languages:
            algo_values.append(mean(algo_result[algo][j]))

        plt.subplot(1, len(algo_result), i+1)
        plt.title(algo)
        plt.ylabel("time (in seconds)")
        plt.bar(algo_languages, algo_values)
    
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
    parser.add_argument("-n", type=int, required=False, default=5000,
                        help="N specifies the size of random elements that get sorted. The default value is 5000.")
    parser.add_argument("-k", type=int, required=False, default=10,
                        help="K specifies the number of algorithm runs. The default value is 10.")
    args = parser.parse_args()

    start_time = time.time()

    print("Getting CPU information...")

    queue = [("C", "Bubblesort"), ("Java", "Bubblesort.class"), ("Python", "Bubblesort.py"),
             ("C", "Quicksort"), ("Java", "Quicksort.class"), ("Python", "Quicksort.py"),
             ("C", "Selectionsort"), ("Java", "Selectionsort.class"), ("Python", "Selectionsort.py",)]

    result = {"algorithms": {"Bubble sort": {"C": [], "Java": [], "Python": []},
                             "Quicksort": {"C": [], "Java": [], "Python": []},
                             "Selection sort": {"C": [], "Java": [], "Python": []}},
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
        f.close()
        args.n = len(numbers)

    print("Starting the algorithms...")

    for i in tqdm(range(1, args.k+1), desc="Total", colour="green", position=1):
        for j in tqdm(queue, desc="(" + str(i) + "/" + str(args.k) + ")", ascii=True, position=0):
            if "Bubblesort" in j[1]:
                result["algorithms"]["Bubble sort"][j[0]].append(measure_real_time(j, str(numbers)))
            elif "Quicksort" in j[1]:
                result["algorithms"]["Quicksort"][j[0]].append(measure_real_time(j, str(numbers)))
            elif "Selectionsort" in j[1]:
                result["algorithms"]["Selection sort"][j[0]].append(measure_real_time(j, str(numbers)))

    elapsed_time = time.time()
    runtime = elapsed_time - start_time

    write_result_to_file(result, init_timedate)
    make_result_plot(result, args.n, args.k, init_timedate)
    tqdm.write("Done. It took " + time.strftime("%Mm:%Ss", time.gmtime(runtime)) +
               ". A benchmark plot was saved in the program directory.")

if __name__ == "__main__":
    main() 