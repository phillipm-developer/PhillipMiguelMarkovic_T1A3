#!/bin/bash

# echo "$(command -v python3)"
# echo "$(command -v bash)"

if ! [[ -x "$(command -v python3)" ]]
then
    echo 'Error: 
        This program runs on Python, but it looks like Python is not installed.
        To install Python, check out https://installpython3.com/' >&2
    exit 1
fi

# if python -c "import pytest" &> /dev/null; then
#     echo ''
# else
#     echo 'PyTest module is not installed'
#     echo "You can install PyTest on the command line using 'pip install pytest'"
#     exit 1 
# fi

# if python -c "import matplotlib" &> /dev/null; then
#     echo ''
# else
#     echo 'MatPlotlib module is not installed'
#     echo "You can install MatPlotlib on the command line using 'pip install matplotlib'"
#     exit 1
# fi

python3 -m venv .venv
source .venv/bin/activate

if python -c "import pytest" &> /dev/null; then
    echo ''
else
    echo 'PyTest module is not installed'
    echo "You can install PyTest on the command line using 'pip install pytest'"
    exit 1 
fi

if python -c "import matplotlib" &> /dev/null; then
    echo ''
else
    echo 'MatPlotlib module is not installed'
    echo "You can install MatPlotlib on the command line using 'pip install matplotlib'"
    exit 1
fi

python3 main.py $1 $2 $3 $4 $5 $6

deactivate
