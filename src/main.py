import expression
import argparse
import csv
import json

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


parser = argparse.ArgumentParser()

parser.add_argument("-e", "--equation", help="Expression to evaluate")
parser.add_argument("-v", "--value", help="Numerical value to subtitute into equation")
parser.add_argument("-vs", "--values", help="Solve for these values")
parser.add_argument("-i", "--inputfile", help="Input file to draw values from")
parser.add_argument("-o", "--outputfile", help="Output file for evaluated answers")

args = parser.parse_args()

# print(args)

args_dict = vars(args)
# print(args_dict)

exp = ""
equation = []

def interactive_mode():
    while (True):
        try:
            exp = input("Please enter an expression> ")

            equation = expression.Expression(exp)

            calculation_dict = {
                'equation' : f"{equation}",
                'result' : 'NONE',
                'solved' : False,
                'values_obtained' : False
            }

            substitutions = equation.extract_variable_names()
            calculation_dict['substitutions'] = substitutions

            print(calculation_dict)

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

            print(calculation_dict)

        except expression.syntax_exception.SyntaxException as err:
            print(err.get_message())

def process_csv_file():
    output_list = []

    # Open the input csv file and read each row from it
    with open('input.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:

            equation = expression.Expression(row['equation'])

            # Begin constructing the calculation dictionary which will be passed into Expression
            calculation_dict = {
                'equation' : f"{equation}",
                'result' : 'NONE',
                'solved' : False,
                'values_obtained' : False
            }

            # Extract variable names from the equation
            substitutions = equation.extract_variable_names()

            # Assign input values to the variables from the file
            for key in substitutions:
                substitutions[key] = row[key]

            # Assign substitutions dictionary back into the calculation dictionary with values set                
            calculation_dict['substitutions'] = substitutions
            calculation_dict['values_obtained'] = True

            # Evaluate the euqation using the data in the calculation dictionary and set the result
            calculation_dict = equation.evaluate_calc_dict(calculation_dict)
            print(calculation_dict)

            row['result'] = calculation_dict['result']
            print(row)
            output_list.append(row)

    f.close()  # Close the file handle for the input file

    # Open the output file and write the header and the results
    with open('output.csv', 'w') as f:
        writer = csv.DictWriter(f, output_list[0].keys())
        writer.writeheader()
        writer.writerows(output_list)

    f.close()  # Close the file handle for the output file


def process_json_file():
    with open('input.json', 'r') as f:
        data = json.load(f)

    for calculation_dict in data:
        equation = expression.Expression(calculation_dict['equation'])
        calculation_dict = equation.evaluate_calc_dict(calculation_dict)
        print(calculation_dict)


    with open('output.json', 'w') as f:
        json.dump(data, f)

# if args_dict['inputfile'] != 'None':
#     input_file = args_dict['inputfile']

# process_csv_file()

process_json_file()

# interactive_mode()
