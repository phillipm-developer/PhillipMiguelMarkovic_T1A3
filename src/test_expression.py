import pytest
from expression import Expression
from syntax_exception import SyntaxError
from syntax_exception import ErrorType

def test_parse_expression():
    exp = Expression('2*x+3')

    infix_list1 = exp.get_infix_list()
    exp.parse_expression('sin(x)-cos(x)')
    infix_list2 = exp.get_infix_list()

    assert not infix_list1 == infix_list2

    exp.parse_expression('2*x+3')
    infix_list2 = exp.get_infix_list()

    assert infix_list1 == infix_list2

def test_is_float():
    exp = Expression("x+1")
    assert exp.is_float('12')
    assert exp.is_float('12.05') == True
    assert exp.is_float('12.0') == True
    assert exp.is_float('-12.05') == True
    assert exp.is_float('-12') == True
    assert exp.is_float('-12.0') == True
    assert exp.is_float('-12.55') == True
    assert exp.is_float('0') == True
    assert exp.is_float('0.0') == True
    assert exp.is_float('-0') == True
    assert exp.is_float('-0.0') == True
    assert exp.is_float('twelve') == False
    assert exp.is_float('100F') == False


def text_extract_variable_names():
    exp = Expression("2*x^2+5*y-sin(y*z)")

    dict = exp.extract_variable_names()

    assert len(dict) == 3
    assert "x" in dict.keys()
    assert "y" in dict.keys()
    assert "z" in dict.keys()

def test_evaluate_list_of_values():
    exp = Expression("x^2")
    values = [1, 2, 3, 4, 5]
    results = exp.evaluate_list_of_values(values)

    assert len(results) == 5
    assert results[0] == 1
    assert results[1] == 4
    assert results[2] == 9
    assert results[3] == 16
    assert results[4] == 25

def test_evaluate_calc_dict():
    # Create an instance of an Expression object
    exp = Expression('x^2+y^2+10')
    infix = exp.get_infix_list()

    # Set up a calculation dictionary
    calculation_dict = {
        'equation' : f"{exp}",
        'result' : 'NONE',
        'solved' : False,
        'values_obtained' : True
    }

    # Extract the variables from the eqaution and create a variable dictionary (substitutions)
    substitutions = exp.extract_variable_names()
    substitutions['x'] = '5'
    substitutions['y'] = '3'
    calculation_dict['substitutions'] = substitutions

    assert not calculation_dict['solved']
    assert calculation_dict['result'] == 'NONE'

    exp.evaluate_calc_dict(calculation_dict)

    assert calculation_dict['solved']
    assert calculation_dict['result'] == 44

def test_evaluate():

    # Set up a postfix list for the equation 'x^2+2*x+1'
    postfix_list = []
    postfix_list.append('5')
    postfix_list.append('2')
    postfix_list.append('^')
    postfix_list.append('2')
    postfix_list.append('5')
    postfix_list.append('*')
    postfix_list.append('+')
    postfix_list.append('1')
    postfix_list.append('+')

    exp = Expression('x^2+2*x+1')
    result = exp.evaluate(postfix_list)

    assert result == 36

def test_create_infix_list():
    equation = '(x+1)/(x-1)'
    exp = Expression(equation)
    exp.infix_list = []
    infix_list = exp.create_infix_list(equation)

    assert len(infix_list) == 11
    assert infix_list[0] == '('
    assert infix_list[1] == 'x'
    assert infix_list[2] == '+'
    assert infix_list[3] == '1'
    assert infix_list[4] == ')'
    assert infix_list[5] == '/'
    assert infix_list[6] == '('
    assert infix_list[7] == 'x'
    assert infix_list[8] == '-'
    assert infix_list[9] == '1'
    assert infix_list[10] == ')'

def test_check_syntax():
    expected_error_msg = "Error at column 5 in x^2**3\n                         ^"
    actual_error_msg = ''
    # Set up Expression instance with a properly formed expression
    exp = Expression('x^2*3')

    # Vacate the member infix list and re-insert a badly formatted version 
    # of the previous expression to force an exception to be
    exp.infix_list = []
    exp.infix_list.append('x')
    exp.infix_list.append('^')
    exp.infix_list.append('2')
    exp.infix_list.append('*')
    exp.infix_list.append('*')
    exp.infix_list.append('3')

    try:
        exp.check_syntax(exp.infix_list)
    except SyntaxError as err:
        actual_error_msg = err.get_message()

    assert actual_error_msg == expected_error_msg

def test_create_postfix_list():
    equation = '(x+1)/(x-1)'
    exp = Expression(equation)
    postfix_list = []

    assert len(postfix_list) == 0

    infix_list = exp.get_infix_list()

    postfix_list = exp.create_postfix_list(infix_list)

    assert len(postfix_list) == 7
    assert postfix_list[0] == 'x'
    assert postfix_list[1] == '1'
    assert postfix_list[2] == '+'
    assert postfix_list[3] == 'x'
    assert postfix_list[4] == '1'
    assert postfix_list[5] == '-'
    assert postfix_list[6] == '/'

def test_precedence_level():
    exp = Expression("x+1")
    assert exp.precedence_level("(") == 0
    assert exp.precedence_level(")") == 0
    assert exp.precedence_level("^") == 3
    assert exp.precedence_level("*") == 2
    assert exp.precedence_level("/") == 2
    assert exp.precedence_level("+") == 1
    assert exp.precedence_level("-") == 1
    assert exp.precedence_level("sin") == 4
    assert exp.precedence_level("cos") == 4
    assert exp.precedence_level("tan") == 4
    assert exp.precedence_level("sqrt") == 4
    assert exp.precedence_level("mu") == 4

def test_get_infix_list():
    exp = Expression("x^2+2*x+12")
    infix_list = exp.get_infix_list()

    assert len(infix_list) == 9
    assert infix_list[0] == 'x'
    assert infix_list[1] == '^'
    assert infix_list[2] == '2'
    assert infix_list[3] == '+'
    assert infix_list[4] == '2'
    assert infix_list[5] == '*'
    assert infix_list[6] == 'x'
    assert infix_list[7] == '+'
    assert infix_list[8] == '12'

def test_get_postfix_list():
    exp = Expression("x^2+2*x+12")
    postfix_list = exp.get_postfix_list()

    assert len(postfix_list) == 9
    assert postfix_list[0] == 'x'
    assert postfix_list[1] == '2'
    assert postfix_list[2] == '^'
    assert postfix_list[3] == '2'
    assert postfix_list[4] == 'x'
    assert postfix_list[5] == '*'
    assert postfix_list[6] == '+'
    assert postfix_list[7] == '12'
    assert postfix_list[8] == '+'


def test_is_operator():
    exp = Expression('x+1')

    assert exp.is_operator('(')
    assert exp.is_operator(')')
    assert exp.is_operator('+')
    assert exp.is_operator('-')
    assert exp.is_operator('/')
    assert exp.is_operator('*')
    assert exp.is_operator('^')
    assert exp.is_operator('sin')
    assert exp.is_operator('cos')
    assert exp.is_operator('tan')
    assert exp.is_operator('sqrt')
    assert exp.is_operator('mu')
    assert not exp.is_operator('notanoperator')
    assert not exp.is_operator(' ')

def test_is_unary_operator():
    exp = Expression('x+1')

    assert not exp.is_unary_operator('(')
    assert not exp.is_unary_operator(')')
    assert not exp.is_unary_operator('+')
    assert not exp.is_unary_operator('-')
    assert not exp.is_unary_operator('/')
    assert not exp.is_unary_operator('*')
    assert not exp.is_unary_operator('^')
    assert exp.is_unary_operator('sin')
    assert exp.is_unary_operator('cos')
    assert exp.is_unary_operator('tan')
    assert exp.is_unary_operator('sqrt')
    assert exp.is_unary_operator('mu')
    assert not exp.is_unary_operator('notanoperator')
    assert not exp.is_unary_operator(' ')

def test_is_binary_operator():
    exp = Expression('x+1')

    assert not exp.is_binary_operator('(')
    assert not exp.is_binary_operator(')')
    assert exp.is_binary_operator('+')
    assert exp.is_binary_operator('-')
    assert exp.is_binary_operator('/')
    assert exp.is_binary_operator('*')
    assert exp.is_binary_operator('^')
    assert not exp.is_binary_operator('sin')
    assert not exp.is_binary_operator('cos')
    assert not exp.is_binary_operator('tan')
    assert not exp.is_binary_operator('sqrt')
    assert not exp.is_binary_operator('mu')
    assert not exp.is_binary_operator('notanoperator')
    assert not exp.is_binary_operator(' ')

def test_is_number_or_variable():
    exp = Expression('x+1')

    assert not exp.is_number_or_variable('(')
    assert not exp.is_number_or_variable(')')
    assert not exp.is_number_or_variable('+')
    assert not exp.is_number_or_variable('-')
    assert not exp.is_number_or_variable('/')
    assert not exp.is_number_or_variable('*')
    assert not exp.is_number_or_variable('^')
    assert not exp.is_number_or_variable('sin')
    assert not exp.is_number_or_variable('cos')
    assert not exp.is_number_or_variable('tan')
    assert not exp.is_number_or_variable('sqrt')
    assert not exp.is_number_or_variable('mu')
    assert exp.is_number_or_variable('33')
    assert exp.is_number_or_variable('-33')
    assert exp.is_number_or_variable('0')
    assert exp.is_number_or_variable('x')
    assert exp.is_number_or_variable('notanoperator')

def test_remove_whitespace():
    exp = Expression('x+1')
    function = "  x^2  + y* 3*z^  2 "

    assert exp.remove_whitespace(function) == "x^2+y*3*z^2"


