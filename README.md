# How to run the project

1. Clone the repository to your local machine.

    ```bash
    git clone https://github.com/daniiprietoo/lab1-AIF.git
    cd lab1-AIF
    ```

## If using a virtual environment

1. Make sure you have Python 3.10 or higher installed (either in conda or system-wide).

    ```bash
    python --version
    ```

    or

    ```bash
    python3 -vV
    ```

2. create and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    c. Run the main script to launch the CLI.

    ```bash
    python main.py
    ```

## If using conda

1. Create and activate the environment:

    ```bash
    conda env create -f environment.yml
    conda activate lab1-AIF
    ```

2. Run the main script to launch the CLI.

    ```bash
    python main.py
    ```

## How to use the CLI

After running `python main.py`, you will see a prompt like this:

```text
Drilling Robot Search
1. Run single example test (using exampleMap.txt)
2. Run single example test (using random n x n grid)
3. Run performance analysis (for 3x3, 5x5, 7x7, 9x9 maps for all algorithms)
Your choice (1/2/3): 
```

You can choose one of the options by entering `1`, `2`, or `3`.

The two first options will prompt again to choose the algorithm to use:

```text
Choose algorithm:
1. Breadth-first search
2. Depth-first search
3. A* search with heuristic
4. Run all algorithms
Your choice (1/2/3/4): 
```

After selecting the algorithm, the program will execute and display the results in the console.

The will prompt again to choose the number of runs desired for each grid size.

```text
Number of simulations per map size (default 5): 
```
