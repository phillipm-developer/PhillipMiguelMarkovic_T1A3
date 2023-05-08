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

# parser.add_argument("-e", "--equation", help="Expression to evaluate")
# parser.add_argument("-v", "--value", help="Numerical value to subtitute into equation")
# parser.add_argument("-vs", "--values", help="Solve for these values")

parser.add_argument("-i", "--input_file", type=str, help="CSV or JSON input file containing equation & values")
parser.add_argument("-o", "--output_file", type=str, help="CSV or JSON output file for evaluated answers")


args = parser.parse_args()
# print(args)

args_dict = vars(args)
print(args_dict)

exp = ""
equation = []

def interactive_mode():
    while (True):
        try:
            exp = input("Please enter an expression> ")

            if exp.lower() == "quit" or exp.lower() == "exit":
                break

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

def process_csv_file(input_csv_file):
    output_list = []

    # Open the input csv file and read each row from it
    with open(input_csv_file) as f:
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

            # Evaluate the equation using the data in the calculation dictionary and set the result
            calculation_dict = equation.evaluate_calc_dict(calculation_dict)
            # print(calculation_dict)

            # row['result'] = calculation_dict['result']
            # print(row)

            output_list.append(calculation_dict)

    f.close()  # Close the file handle for the input file
    return output_list

    # Open the output file and write the header and the results
    # with open('output.csv', 'w') as f:
    #     writer = csv.DictWriter(f, output_list[0].keys())
    #     writer.writeheader()
    #     writer.writerows(output_list)

    # f.close()  # Close the file handle for the output file

# Open the output file and write the header and the results
def write_csv_file(output_list, output_csv_file):
    write_list = []
    for dict in output_list:
        row = f"{output_list},"

    # with open(output_csv_file, 'w') as f:
    #     writer = csv.DictWriter(f, output_list[0].keys())
    #     writer.writeheader()
    #     writer.writerows(output_list)

    # f.close()  # Close the file handle for the output file

def process_json_file(input_json_file):
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    for calculation_dict in data:
        equation = expression.Expression(calculation_dict['equation'])
        calculation_dict = equation.evaluate_calc_dict(calculation_dict)
        print(calculation_dict)

    f.close()
    return data

    # with open('output.json', 'w') as f:
    #     json.dump(data, f)


def write_json_file(data, output_json_file):
    with open(output_json_file, 'w') as f:
        json.dump(data, f)


input_file = args_dict['input_file']
output_file = args_dict['output_file']

output_list = []

if input_file != None:  # None is a python keyword meaning null value
    if '.json' in input_file:
        output_list = process_json_file(input_file)
    elif '.csv' in input_file:
        output_list = process_csv_file(input_file)    

if output_file != None:
    if '.json' in output_file:
        write_json_file(output_list, output_file)
    elif '.csv' in output_file:
        write_csv_file(output_list, output_file)

# interactive_mode()
