from sys import argv

# Parses arguments from the command line returning a arggument dictionary
def parse_args():
    argumentList = argv[1:]
    arg_dict = { "-i" : None, "-o" : None, "-png" : None }

    for index, argument in enumerate(argumentList):
        if argument in arg_dict and index+1 < len(argumentList) and not argumentList[index+1] in arg_dict:
            if argument == "-i" and arg_dict['-i'] == None:
                arg_dict["-i"] = argumentList[index+1]
            elif argument == "-o" and arg_dict['-o'] == None:
                arg_dict["-o"] = argumentList[index+1]
            elif argument == "-png" and arg_dict['-png'] == None:
                arg_dict["-png"] = argumentList[index+1]
        elif argument == "-h":
            print("Usage: main.py [-h] [-png PNG_IMAGE] [-i INPUT_FILE] [-o OUTPUT_FILE]")

    return arg_dict

# parse_args()
