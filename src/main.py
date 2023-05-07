import expression
import argparse
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

# exp = "-sin(90) + xx^2 +10  *x+2-10*zz * (7-8)*-sin(45)"

# exp = "-sin(90) + 5^2 +10  *6+2-10*4 * (7-8)*-sin(45)"

# exp = "(12-7)*-sin(30)"

exp = ""
equation = []

# while (True):
#     exp = input("Please enter an expression> ")
#     equation = expression.Expression(exp)
#     print(equation.get_infix_list())

try:
    # exp = ")99"
    exp = "(12-7)*-sin(30)-"
    equation = expression.Expression(exp)
    equation.assign_infix_list()
except expression.syntax_exception.SyntaxException as err:
    print(err.get_message())



# print(expression)

# print(exp)
# print(exp.replace(" ", ""))
# print(exp)
