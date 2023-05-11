# PhillipMiguelMarkovic_T1A3

# References

https://www.tutorialspoint.com/coding-standards-style-guide-for-python-programs

https://peps.python.org/pep-0008/

https://www.coderacademy.edu.au/faq - Hardware and OS Requirements

# Link to Source Control Repository

https://github.com/phillipm-developer/PhillipMiguelMarkovic_T1A3

# Code Style Guide

The expression evauator teminal application adheres to the PEP8 coding standards document (Python Enhancment Proposal 8).

The following standards were employed in the terminal application code during it's implementation.

## Naming of Collections

At no point does the code use individual letters or names that lack any meaning. All variables regardless of scope use semantically meaningful names, even if the variable names are lengthy. This applies to collection classes (lists, tuples & dictionaries). For example:

self.infix_list = infix_list

A locally scoped list assigned as a member variable.

calculation_dict['substitutions'] = substitutions_dict

Assigning a dictionary of substitutions (variable names and the values assigned to them) to a calculation dictionary. 

Note the use of '_list' and '_dict' to denote the data collection type and the elements they contain.

## Packages and Modules

All packages and modules are declared at the top of each source file. They all use lower case names with underscores between words to improve readability and meaning.

Where it is practical modules are imported in the following manner (known as absolute imports):

from expression import Expression<br>
from syntax_exception import SyntaxException<br>
from syntax_exception import ErrorType

This enables a developer to reference classes, their methods and other functions directly instead of specifying the module name first. This improves readability and reduces the clutter (spagetti) in the code. It also reduces performance overhead by restricting the use of a module to only those things the program requires.

Mutiple imports are done line by line for clarity. Modules are also imported in the following order:

Built-in module imports<br>
Thirty party module imports<br>
Module imports locally developed 

At no point does the terminal app use wildcards(*) in it's imports. This maintains clarity on what resoources are being imported into the namespace.

## Naming Conventions (General)

Classes are named using pascal case where the first letter of each word is capitalised e.g. class PascalCase:

Exception classes are named such that each name ends with the letters 'Error'. Here class SyntaxError inherits from Exception 
e.g. class SyntaxError(Exception)

Both function and variable names follow the same naming convention. Names are all lower case with words being separated by underscores. Private member variables and methods are prefixed with underscores to prevent direct access.

## Indenting

The code for the terminal application uses 4 spaces per indentation as per PEP8. The VSCode development environment (used to develop the terminal app), converts all tabs to spaces, so no source file ever has any tabs and therefore no mixing of tabs and spaces ever arises. This is not permitted in Python.

There are no unecessary spaces in expressions and statements.

## Comments

Comments in the terminal app are no more than 79 characters for function/method headers. They are no more than 72 characters for inline comments. If these limits are exceeded, the comment will wrap onto the next line.

The approach taken during development was to write comments as an outline (or pseudocode) of steps which mirrored the project plan. These initial comments act as headers for the various functions and methods that were created underneath them. Comments are not used for statements which are self explanatory.

# Major Features

The terminal application that was implemented is an expression evaluator designed for ease of use. It does this by providing the following major features to the general user.

## File Input and Output

The expression evaluator is capable of reading a set of data from an input file specified on the command line. This allows the app to obtain the multiple expressions to be evaluated and the corresponding variables, as well as the values to be substituted into those values.

Each record is read into a data structure called a calculation dictionary. This acts as a workspace from which the app can read the expression to evaluate and the values to substitute into the expression. Once the expression is evaluated, the result is written back into the calculation dictionary.

Once all the evaluations are carried out, the list of calculation dictionaries is then written out to a file suupplied on the command line.

The basic logical structure of a calculation dictionary is as follows:

    calculation_dict[
            {
                'equation': 'sin(x^2)+sin(x*y)-cos(y^2)', 
                'result': -2.49548102969227, 
                'solved': True, 
                'values_obtained': True, 
                'substitutions': {'x': '7', 'y': '3.5'}
            }
        ]

This is what a calculation dictionary looks like after evaluation and just before it is written to the output file.

If only an input file is supplied on the command line but no output file, then the output is displayed to screen.

If an output file is supplied without a corresponding input file an error occurs and a message is displayed in the console.

This application uses the JSON file formats for all its inputs and outputs. It is the most practical way to manage arbitrary numbers of variables. It is a data format that is supported by many programming languages and allows the data generated by this app to be transferred between systems.

## Interactive Mode

If no command line parameters are supplied to the app when it is invoked, it will enter interactive mode. This is a simple shell which accepts values. The user will be prompted for an expression which they supply being careful to make sure it is properly formatted.

The app will extract the variables from the expression, then prompt the user for a value to substitute into each variable. This information is inserted into a new calculation dictionary object which is then passed to the expression evalator part of the app for processing. It writes the result back into the dictionary. The app then retrieves this result and displays it in the console. The user is then prompted for the next expression. Here is a sample run in interactive mode:

    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$ ./evaluate.sh
    Please enter an expression> x^3+3*x^2-y^2+sin(y)+z
    Please enter the value for x> 12
    Please enter the value for y> 9
    Please enter the value for z> 5
    2084.4121184852415
    Please enter an expression> quit
    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$

This loop will continue until the user types 'quit' or 'exit' at the prompt, at which point the program will terminate.

If the user submits an improperly formatted expression such as an extra operator in the wrong place or a missing parentheses a syntax error (exception) is generated and an appropriate error message is displayed as in the following run:

    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$ ./evaluate.sh
    Please enter an expression> x^2+3**x-15
    Error at column 7 in x^2+3**x-15
                               ^
    Please enter an expression>

## Support for Unlimited Variables

The expression evaluator terminal app supports any number of variables with user defined names in expressions.

e.g. 3*x+4*(a-dog)-10*sin(cat)

The app converts the string expression into a list of tokens called an infix list, where each token becomes an operator or operand. Each operand is either a number or variable.

The expression evaluator component has a method which extracts the variables out of an expression and creates 'substitutions_dict' dictionary which is then inserted into the parent calculation dictionary. In this case:

[{'x' : 'NONE', 'a' : 'NONE', 'dog' : 'NONE', 'cat' : 'NONE'}]

The values are set later, but prior evaluation.

## Image File of Plotted Function Generation

Another unique feature of this app is the ability to generate an image file which is created in the current working directory of the program. The user specifies the -png option followed by the expression you wish to plot.

Internally the app will by default (unless otherwise specified) create a list of 100 values in the range -50 to 50. The app will then use the expression submitted on the command line to evaluate each value to produce a list of 100 results. The results are plotted against the initial values. A Portable Network Graphic (PNG) file is generated and stored to the file system.

Here is a sample png image for the function y = x^2 generated by the app:

![Alt text](docs/Figure_2023-5-10_16-24-39%3A372930.png)

This is accomplished by using a popular third party package called matplotlib. Matplotlib is a plotting library for creating mathematical visualizations.

Each image is generated with its own unique file name. This was achieved by using the built-in module datetime. The file name consists of day, month, year, hr, min, sec and microsecond. This ensures unique filenames are consistently created even if the images are generated in quick succession. The file name for image displayed above is called Figure_2023-5-10_16-24-39:372930.png.

# Implementation Plan

# User Guide

## Installation

The following files are required to run the evaluate terminal application:

evaluate.sh<br>
main.py<br>
expression.py<br>
syntax_exception.py<br>
math_exception.py<br>
plot_equation.py<br>
input.json

These files are available in PhillipMiguelMarkovic_T1A3.zip. Create or choose a designated folder for the app, then extract these files from the archive.

## Dependencies

These files require Python 3.10 or higher, and the python modules pytest and matplotlib. Run the evaluate app from your Linux or WSL (Windows Subsystem for Linux) terminal in the following manner. Move into your nominated directory and run the following:

./evaluate.sh

As part of the initial setup it checks for these dependencies and will display an error to the console advising the user which dependencies are not available. If all 3 are installed the evaluate app will start up in interactive mode.

## System Requirements

Windows 10 or 11 running Windows Subsystem for Linux (WSL).

Alternatively you can use Linux (preferably Ubuntu).

Desktop PC or laptop. I recommend that the hardware be no older than 2019 as this is the specification recommended by Coder Academy to their cohorts for their courses (Refer to 'References' above). This app was developed and tested on an MSI 13th Gen Intel(R) Core(TM) i7-13620H 2.40 GHz laptop so the hardware requirement is reasonable.

So to summarize more generally the minimum requirements are:

Minimum Windows specifications
16GB RAM
No more than 4 years old
Supports Windows 10 or 11  

Minimum Mac specifications:

16GB RAM
No more than 4 years old
OS Big Sur (minimum)

The Mac specification is specified as everyone has different preferences as users may want to run the terminal app on their Mac. The functionality of the app is not guaranteed and the evaluate shell script is unlikely to run on a Mac.

## Usage

The following instructions demonstrate how to use the terminal application with the available comand line options:

./evaluate.sh

If the application is invoked without any arguments supplied on the command line, the terminal app will enter interactive mode. The user is provided with a simple shell and is prompted to supply expressions with variables. The ap will then prompt the user for values for each of the variables in the expression. Once the last value is supplied, the expression is evaluated and the result is displayed as shell output. The user is then prompted for the next expression.

    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$ ./evaluate.sh 
    Please enter an expression> x^2
    Please enter the value for x> 3
    9.0
    Please enter an expression> -x^2
    Please enter the value for x> 3
    9.0
    Please enter an expression> -x^3
    Please enter the value for x> 3
    -27.0
    Please enter an expression> -sin(x)
    Please enter the value for x> 3
    -0.1411200080598672
    Please enter an expression> quit
    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$

The user can type 'quit' or 'exit' at any time to exit the program.

./evaluate.sh -i input.json

The user can invoke the program by specifying the -i command line option and providing the json file as the input paarameter. The app will then open the file and read the input data on each line. The expression, input values and results are then displayed in the console.

    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$ ./evaluate.sh -i input.json 
    EXPR: x^2+2*x+1, VARS: x=5, RESULT: 36.0
    EXPR: -sin(x)-cos(x)+sin(3*x), VARS: x=10, RESULT: 0.3950610158729603
    EXPR: 2*x^3+5*x^2-3*x+10, VARS: x=12, RESULT: 4150.0
    EXPR: 2*x^3+5*x^2-3*x+10, VARS: x=15, RESULT: 7840.0
    EXPR: 2*x^3+5*x^2-3*x+10, VARS: x=20.5, RESULT: 19280.0
    EXPR: sin(x^2)+sin(x)-cos(x), VARS: x=7, RESULT: -1.0506683083839874
    EXPR: sin(x^2)+sin(x*y)-cos(y^2), VARS: x=7, y=3.5, RESULT: -2.49548102969227
    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$

./evaluate.sh -i output.json -o output.json

By providing and additional parameter -o followed by the output file name, the results of the bulk evaluations will be written to the output file in the current working directory. The results will not be displayed to the console.

./evaluate.sh -o output.json

Supplying and output file without a corresponding input  file is not permitted and an error message will be displayed.

    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$ ./evaluate.sh -o output.json 
    You must provide a corresponding input file '-i' in order to write to output.json
    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$

./evaluate.sh -png "3*x^3-x+10"

The -png option allows the user to specify an equation for the purpose of plotting it on an x-y axis and saving it as an image file to the current working directory. Please ensure you enclose the equation in quotes when declaring it on the command line.

    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$ ./evaluate.sh -png "x^2"
    The figure has been saved to Figure_2023-5-11_22-53-20:30463.png
    phillip@MSI:~/projects/PhillipMiguelMarkovic_T1A3/src$

There is no need to specify an output filename. It ia automaticallly generated by the application.
