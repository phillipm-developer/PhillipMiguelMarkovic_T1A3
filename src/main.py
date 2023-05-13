import csv
import json
import plot_equation
from parse_cmd_line import parse_args
from expression import Expression
from syntax_exception import SyntaxError
from math_exception import MathError

exp = ""
equation = []

# Function for interactive mode
def interactive_mode():
    while (True):
        try:
            exp = input("Please enter an expression> ")

            # Checks if user wants to exit the program
            if exp.lower() == "quit" or exp.lower() == "exit":
                break

            # Create an instance of an Expression object
            equation = Expression(exp)
            infix = equation.get_infix_list()

            # Set up a calculation dictionary
            calculation_dict = {
                'equation' : f"{equation}",
                'result' : 'NONE',
                'solved' : False,
                'values_obtained' : False
            }

            # Extract the variables from the eqaution and create a variable dictionary (substitutions)
            substitutions = equation.extract_variable_names()
            calculation_dict['substitutions'] = substitutions

            # If the values in the equation are not set get them from the user
            if calculation_dict['values_obtained'] == False:
                substitutions = calculation_dict['substitutions']
                for key in substitutions:
                    value = "not_a_number"
                    while not equation.is_float(value):
                        value = input(f"Please enter the value for {key}> ")

                        # Checks if user wants to exit the program
                        if value.lower() == "quit" or value.lower() == "exit":
                            return

                        if not equation.is_float(value):
                            print("Value entered is not a number. Try again.")

                    # Assign value to the variable 
                    substitutions[key] = value

                calculation_dict['substitutions'] = substitutions
                calculation_dict['values_obtained'] = True

            try:
                calculation_dict = equation.evaluate_calc_dict(calculation_dict)
                print(calculation_dict['result'])
            except ValueError as err:
                print(err)

        except SyntaxError as err:
            print(err.get_message())
        except MathError as err:
            print(err.get_message())
        except Exception as err:
            print(err)

# Read and evaluate json file input. 
def process_json_file(input_json_file):
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    f.close()  # close the file as we have loaded the data

    # Evaluates each line (calculation dictionary) in data and writes the result back into the calcualtion dictionary
    for calculation_dict in data:
        equation = Expression(calculation_dict['equation'])
        calculation_dict = equation.evaluate_calc_dict(calculation_dict)

    return data

# Write the solved equations back to an output json file
def write_json_file(data, output_json_file):
    with open(output_json_file, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    # Assign command line parameters to a dictionary for easy program access
    args_dict = parse_args()

    # Assign command line parameters to variables
    input_file = args_dict['-i']
    output_file = args_dict['-o']
    png_equation = args_dict['-png']

    output_list = []

    if input_file != None:  # None is a python keyword meaning null value
        try:
            if '.json' in input_file:
                output_list = process_json_file(input_file)
            else:
                print("Please ensure the you provide a JSON input file using the '.json' extension")

            # Cannot specify an output file without specifying an input file on the cmd line
            # So this code will only run if an input file is provided
            if output_file != None:
                if '.json' in output_file:
                    write_json_file(output_list, output_file)
                    print(f"{output_file} written to the current working directory")
                else:
                    print("Please ensure the you provide a JSON output file using the '.json' extension")
            else:
                for dict in output_list:
                    row_string = f"EXPR: {dict['equation']}, "
                    variables = dict['substitutions']
                    variable_string = 'VARS: '
                    for key, value in variables.items():
                        variable_string += f"{key}={value}, "
                    row_string += variable_string
                    row_string += "RESULT: " + str(dict['result'])
                    print(row_string)

        except FileNotFoundError as err:
            print(err)
        except SyntaxError as err:
            print(err.get_message())

    elif png_equation != None:
        try:
            plot_equation.plot_and_save(png_equation, -100, 100)
        except SyntaxError as err:
            print(err.get_message())
        except MathError as err:
            print(err.get_message())
        except ValueError as err:
            print(err)
        except AttributeError as err:
            print(err)

    elif output_file != None:
        print(f"You must provide a corresponding input file '-i' in order to write to {output_file}")
    else:
        interactive_mode()
