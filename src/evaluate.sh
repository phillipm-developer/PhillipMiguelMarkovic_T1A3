#!/bin/bash

# Checks if python3 is installed
if ! [[ -x "$(command -v python3)" ]]
then
    echo 'Error: 
        This program runs on Python, but it looks like Python is not installed.
        To install Python, check out https://www.python.org/downloads/' >&2
    exit 1
fi

python3 -m venv .venv
source .venv/bin/activate

python3 -c "import pytest" &> /dev/null

# Checks the exit status of the last command
if [ $? -eq 1 ]
    then
        echo 'Error: PyTest module is not installed'
        echo "You can install PyTest on the command line using 'pip install pytest'"
        exit 1
fi

python3 -c "import matplotlib" &> /dev/null

# Checks the exits status of the last command
if [ $? -eq 1 ]
    then
        echo 'Error: MatPlotlib module is not installed'
        echo "You can install MatPlotlib on the command line using 'pip install matplotlib'"
        exit 1
fi

python3 main.py $1 $2 $3 $4 $5 $6

deactivate
