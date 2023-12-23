# Sorting Algorithms

Multiple sorting algorithms implemented in multiple programming languages with an additional speed bechmarking tool that creates presentable plots.

Windows, MacOS, and Linux are all supported.

## Getting started

### Prerequisites

- [Python](https://www.python.org/)
- [Matplotlib](https://matplotlib.org/)
- [Java](https://www.java.com/)
- [GCC](https://gcc.gnu.org/) (optional, if you already own the compiled C code)

### Installing and running

    $ git clone https://github.com/lean-he/sorting-algorithms.git
    $ cd sorting-algorithms
    $ python Benchmark.py

A `result.png` image with a benchmark plot will be saved in the program directory.

## Usage
### Commands
    $ python Benchmark.py [-h] [--no-compile] [--no-number-gen] [-n N]

- `--no-compile` : no compilation of the source files. For a correct functionality is a compilation on the first execution needed.
- `--no-number-gen` : no generation of a new data set. The last used one will be used again. On the first execution is a generation however necessary.
- `-n N` : N specifies the size of random elements that get sorted. The default value is 10000.

### Folder structure

- The `src` folder contains the source code of the algorithms, subdivided into the programming languages.
- The `build` folder contains the binary files after the compilation.
- In the `data` folder is the data set `numbers.txt` saved.