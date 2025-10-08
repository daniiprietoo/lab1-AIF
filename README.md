# How to run the project

1. Clone the repository to your local machine.

    ```bash
    git clone https://github.com/daniiprietoo/lab1-AIF.git
    cd lab1-AIF
    ```

2. Make sure you have Python 3.10 or higher installed (either in conda or system-wide).

3(a). If using a virtual environment:

    a. create and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

    b. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    c. Run the main script to launch the CLI.

    ```bash
    python main.py
    ```

3(b). If using conda:

    a. create and activate the environment:

    ```bash
    conda env create -f environment.yml
    conda activate lab1-AIF
    ```

    b. Run the main script to launch the CLI.

    ```bash
    python main.py
    ```
