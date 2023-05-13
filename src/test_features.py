import os.path
import pytest
import plot_equation
from expression import Expression
from syntax_exception import SyntaxError
from syntax_exception import SyntaxErrorType
from math_exception import MathError
from math_exception import MathErrorType
from plot_equation import plot_and_save
from main import process_json_file
from main import write_json_file

### This pytest script covers the R15 of the Code Requirements ###

### The first 3 tests concern the image creation feature ###

# The following tests what happens when a user runs the following 
# on the command line.
# 
#  ./evaluate.sh -png "x^3+x^2-100*x-12"

# This tests for success. This function tests for the existence of the
# generated image file.
def test_create_image_success():
    png_equation = "x^3+x^2-100*x-12"
    file_name = ""

    try:
        file_name = plot_equation.plot_and_save(png_equation, -100, 100)
    except SyntaxError as err:
        print(err.get_message())
    except MathError as err:
        print(err.get_message())

    path = f"./{file_name}"
    check_file = os.path.isfile(path)  # Returns a Boolean True if file exists

    assert check_file  # Check file ws created in current directory

# This function tests if image creation fails when passing in a function 
# with more than one variable. This is what happens when the user runs 

# ./evaluate.sh -png "x+y+z"

def test_create_image_fail_1():
    png_equation = "x+y+z"
    file_name = ""

    try:
        file_name = plot_equation.plot_and_save(png_equation, -100, 100)
    except MathError as err:
        assert err.get_message() == "Not permitted more than one variable"

# This tests if a misplaced '*' in the expression will halt image 
# file generation. This happens when the user runs 
#
# ./evaluate.sh -png "sin(x)+*cos(x)" 
# 
def test_create_image_fail_2():
    png_equation = "sin(x)+*cos(x)"
    file_name = ""
    expected_error_msg = "Error at column 6 in sin(x)+*cos(x)\n                            ^"
    actual_error_msg = ""

    print(expected_error_msg)

    try:
        file_name = plot_equation.plot_and_save(png_equation, -100, 100)
    except SyntaxError as err:
        actual_error_msg = err.get_message()

    assert actual_error_msg == expected_error_msg

### The next 2 tests concern the file input/output feature ###

# This tests the file input and output feature. The process_json_file
# function reads the input file, evaluates each line and writes the results
# to the output json file specified. It then checks for the  existence of 
# the output file. This is what happens when the command 
#
# ./evaluate -i input.json -o output.json is run
#
def test_json_file_input():
    input_file = "input.json"
    output_file = "output.json"

    data = process_json_file(input_file)
    write_json_file(data, output_file)

    path = f"./{output_file}"
    check_file = os.path.isfile(path)  # Returns a Boolean True if file exists

    assert check_file  # Check file ws created in current directory

# The file defective_input_data.json has an improperly formatted expression.
# This function tests what occurs when the app attempts to read and process 
# it. The behavious here is what would happen if the user runs the following
# command.
#
# ./evaluate -i defective_input_data.json -o output.json
#
def test_defective_json_file_input():
    input_file = "defective_input_data.json"
    output_file = "output.json"
    expected_error_msg = "Error at column 7 in x^2+2**x+1\n                           ^"
    actual_error_msg = ""

    try:
        data = process_json_file(input_file)
        write_json_file(data, output_file)

        path = f"./{output_file}"
        check_file = os.path.isfile(path)  # Returns a Boolean True if file exists
    except SyntaxError as err:
        actual_error_msg = err.get_message()

    assert actual_error_msg == expected_error_msg

