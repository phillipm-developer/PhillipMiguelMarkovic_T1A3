import expression
import argparse
import csv

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

            # print(equation.get_infix_list())
            # print(equation.get_postfix_list())

            print(calculation_dict)

        except expression.syntax_exception.SyntaxException as err:
            print(err.get_message())

if args_dict['inputfile'] != 'None':
    input_file = args_dict['inputfile']

interactive_mode()
