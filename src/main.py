import expression
import argparse
import csv
import json

parser = argparse.ArgumentParser()

# parser.add_argument("-e", "--equation", help="Expression to evaluate")
# parser.add_argument("-v", "--value", help="Numerical value to subtitute into equation")
# parser.add_argument("-vs", "--values", help="Solve for these values")

parser.add_argument("-i", "--input_file", type=str, help="CSV or JSON input file containing equation & values")
parser.add_argument("-o", "--output_file", type=str, help="CSV or JSON output file for evaluated answers")


args = parser.parse_args()

exp = ""
equation = []

def interactive_mode():
    while (True):
        try:
            exp = input("Please enter an expression> ")

            if exp.lower() == "quit" or exp.lower() == "exit":
                break

            equation = expression.Expression(exp)

            # Set up a calculation dictionary
            calculation_dict = {
                'equation' : f"{equation}",
                'result' : 'NONE',
                'solved' : False,
                'values_obtained' : False
            }

            substitutions = equation.extract_variable_names()
            calculation_dict['substitutions'] = substitutions

            if calculation_dict['values_obtained'] == False:
                substitutions = calculation_dict['substitutions']
                for key in substitutions:
                    value = input(f"Please enter the value for {key}> ")
                    substitutions[key] = value
                calculation_dict['substitutions'] = substitutions
                calculation_dict['values_obtained'] = True

            calculation_dict = equation.evaluate_calc_dict(calculation_dict)

            evaluation_list = []
            evaluation_list.append(calculation_dict)

            print(calculation_dict['result'])

        except expression.syntax_exception.SyntaxException as err:
            print(err.get_message())

# Read and evaluate json file input. 
def process_json_file(input_json_file):
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    # Evaluates each line (calculation dictionary) in data and writes the result back into the calcualtion dictionary
    for calculation_dict in data:
        equation = expression.Expression(calculation_dict['equation'])
        calculation_dict = equation.evaluate_calc_dict(calculation_dict)

    f.close()
    return data

# Write the solved equations back to an output json file
def write_json_file(data, output_json_file):
    with open(output_json_file, 'w') as f:
        json.dump(data, f)


args_dict = vars(args)
# print(args_dict)


input_file = args_dict['input_file']
output_file = args_dict['output_file']

output_list = []

if input_file != None:  # None is a python keyword meaning null value
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
else:
    interactive_mode()
