import expression
import argparse
import csv
import json
import plot_equation

parser = argparse.ArgumentParser()

# parser.add_argument("-e", "--equation", help="Expression to evaluate")
# parser.add_argument("-v", "--value", help="Numerical value to subtitute into equation")
# parser.add_argument("-vs", "--values", help="Solve for these values")

parser.add_argument("-png", "--png_image", help="Expression to plot and save as image file")
parser.add_argument("-i", "--input_file", type=str, help="CSV or JSON input file containing equation & values")
parser.add_argument("-o", "--output_file", type=str, help="CSV or JSON output file for evaluated answers")


args = parser.parse_args()

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
            equation = expression.Expression(exp)
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
                    value = input(f"Please enter the value for {key}> ")

                    # Checks if user wants to exit the program
                    if value.lower() == "quit" or value.lower() == "exit":
                        return

                    # Assign value to the variable 
                    substitutions[key] = value

                calculation_dict['substitutions'] = substitutions
                calculation_dict['values_obtained'] = True

            try:
                calculation_dict = equation.evaluate_calc_dict(calculation_dict)
                print(calculation_dict['result'])
            except ValueError as err:
                print(err)

        except expression.syntax_exception.SyntaxException as err:
            print(err.get_message())

# Read and evaluate json file input. 
def process_json_file(input_json_file):
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    f.close()  # close the file as we have loaded the data

    # Evaluates each line (calculation dictionary) in data and writes the result back into the calcualtion dictionary
    for calculation_dict in data:
        equation = expression.Expression(calculation_dict['equation'])
        calculation_dict = equation.evaluate_calc_dict(calculation_dict)

    return data

# Write the solved equations back to an output json file
def write_json_file(data, output_json_file):
    with open(output_json_file, 'w') as f:
        json.dump(data, f)


# Assign command line parameters to a dictionary for easy program access
args_dict = vars(args)

input_file = args_dict['input_file']
output_file = args_dict['output_file']
png_equation = args_dict['png_image']

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
    except expression.syntax_exception.SyntaxException as err:
        print(err.get_message())

elif png_equation != None:
    plot_equation.plot_and_save(png_equation, -100, 100)
    print("made it to here")
else:
    interactive_mode()
