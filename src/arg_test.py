import argparse

parser = argparse.ArgumentParser()

# parser.add_argument('--foo')
parser.add_argument("-png", "--png_expression", help="Expression to plot and save as image file")
parser.add_argument("-i", "--input_file", type=str, help="CSV or JSON input file containing equation & values")
parser.add_argument("-o", "--output_file", type=str, help="CSV or JSON output file for evaluated answers")


# args, unknown = parser.parse_known_args(['--foo', 'BAR', 'spam'])

args, unknown = parser.parse_known_args()

print(args)
# Namespace(foo='BAR')
print(unknown)
# ['spam']