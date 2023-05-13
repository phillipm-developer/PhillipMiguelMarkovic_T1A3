from math_exception import MathError
from math_exception import ErrorType
from syntax_exception import SyntaxError
from syntax_exception import ErrorType
import math
import numbers

class Expression:
    def __init__(self, expression):
        self.expression = expression
        self.infix_list = []
        self.postfix_list = []

        self.operator_list = [
            "",
            "(",
            ")",
            "^",
            "*",
            "/",
            "+",
            "-",
            "sin",
            "cos",
            "tan",
            "sqrt",
            "mu"
        ]

        # Initisalisation
        self.values_set = False
        self.expression = self.remove_whitespace(self.expression)
        self.infix_list = self.create_infix_list(self.expression)
        self.postfix_list = self.create_postfix_list(self.infix_list)

    # Allows same instance of Expression to be used with a new function
    def parse_expression(self, expression):
        if len(self.infix_list) > 0:
            self.infix_list = []

        if len(self.postfix_list) > 0:
            self.postfix_list = []

        self.expression = expression
        
        # Re-initialise the expression
        self.values_set = False
        self.expression = self.remove_whitespace(self.expression)
        self.infix_list = self.create_infix_list(self.expression)
        self.postfix_list = self.create_postfix_list(self.infix_list)

    # End-user readable representation of the object
    def __str__(self):
        return self.expression

    # Utitiy function for converting strings to floats
    def is_float(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    # Extract all the variable name from the postfix list then create a dictionary  
    # from them, then return said dictionary
    def extract_variable_names(self):
        variable_names = {}
        for index, element in enumerate(self.postfix_list):
            if element not in self.operator_list and not self.is_float(element):
                if element not in variable_names.items():
                    variable_names[element] = 'NONE'
        return variable_names

    # This method takes a list of values and calculates the results for each, returning the results
    # in a list of equivalent size (Note: This method assumes the expression only has one variable in it)
    def evaluate_list_of_values(self, value_list):
        result_list = []

        # Extract the variables from the eqaution and create a variable dictionary (substitutions)
        substitutions = self.extract_variable_names()

        if len(substitutions) > 1:
            print("Please submit an expression with only one variable in it")
        elif len(substitutions) == 1:
            var_name = list(substitutions.keys())[0]

            # Calculate for each value in value_list
            for value in value_list:
                postfix_list = []
                postfix_list = self.postfix_list.copy()  # Local copy of postfix list
                for index, element in enumerate(postfix_list):
                    if element == var_name:
                        postfix_list[index] = value

                result = self.evaluate(postfix_list)        
                result_list.append(result)

        return result_list


    # This returns a calculation dictionary with the result of the calculation
    def evaluate_calc_dict(self, calculation_dict):
        postfix_list = self.postfix_list
        substitutions = calculation_dict['substitutions']

        # Substitute all variables in the equation with their assigned values
        for key, value in substitutions.items():
            for index, element in enumerate(postfix_list):
                if element == key:
                    postfix_list[index] = value

        # Local postfix list has nothing but numbers and operands in it, so
        # it can now be evaluated    
        result = self.evaluate(postfix_list)

        # Assign result back into calculation dictionary
        calculation_dict['result'] = result
        calculation_dict['solved'] = True

        return calculation_dict


    # Evaluates the postfix list (Note: This method assumes that all the 
    # operands are numbers)
    def evaluate(self, postfix_list):
        operand_stack = []
        final_result = 0

        for index, element in enumerate(postfix_list):
            if not self.is_operator(element):
                operand_stack.append(float(element))
            else:
                match element:
                    case "+":
                        operand_2 = operand_stack.pop()
                        operand_1 = operand_stack.pop()
                        result = operand_1 + operand_2
                        operand_stack.append(result)

                    case "-":
                        operand_2 = operand_stack.pop()
                        operand_1 = operand_stack.pop()
                        result = operand_1 - operand_2
                        operand_stack.append(result)

                    case "*":
                        operand_2 = operand_stack.pop()
                        operand_1 = operand_stack.pop()
                        result = operand_1 * operand_2
                        operand_stack.append(result)

                    case "/":
                        operand_2 = operand_stack.pop()
                        operand_1 = operand_stack.pop()

                        if operand_2 == 0:
                            raise MathError(ErrorType.Divide_By_Zero)
                        
                        result = operand_1 / operand_2
                        operand_stack.append(result)

                    case "^":
                        operand_2 = operand_stack.pop()
                        operand_1 = operand_stack.pop()
                        result = pow(operand_1, operand_2)
                        operand_stack.append(result)

                    case "sin":
                        operand = operand_stack.pop()
                        result = math.sin(operand)
                        operand_stack.append(result)

                    case "cos":
                        operand = operand_stack.pop()
                        result = math.cos(operand)
                        operand_stack.append(result)

                    case "tan":
                        operand = operand_stack.pop()
                        result = math.tan(operand)
                        operand_stack.append(result)

                    case "sqrt":
                        operand = operand_stack.pop()
                        result = math.sqrt(operand)
                        operand_stack.append(result)

                    case "mu":
                        operand = operand_stack.pop()
                        result = -1 * operand
                        operand_stack.append(result)

        final_result = operand_stack.pop()

        return final_result
    
    # Converts the expression to infix form for later use
    def create_infix_list(self, infix_string):
        infix_list = []  # Set up local infix list
        token = ''  # Appended to character by character to form a string

        for element in infix_string:
            if self.is_operator(element):
                if len(token) > 0:
                    infix_list.append(token)
                    token = ''

                infix_list.append(element)
            else:
                token += element

        if len(token) > 0:
            infix_list.append(token)
            token = ''

        # Check that the expression is properly formed
        if not self.check_syntax(infix_list):
            return


        # Insert unary minus operators
        for index, element in enumerate(infix_list):
            if element == "-":
                if index == 0:
                    infix_list[index] = "mu"
                elif index > 0 and index < len(infix_list)-1 and self.is_operator(infix_list[index-1]) and infix_list[index-1] != ")":
                    infix_list[index] = "mu"

        # Insert parentheses to encompass the operand for a unary minus operator. A unary minus is treated as a 
        # function the way sin & cos are as they only apply to a single operator as well

        stemp = []  # We treat this variable as a stack
        vtemp = []  # We construct the new list consisting of expression tokens with the parentheses inserted for unary minus (mu)

        for index, element in enumerate(infix_list):
            if infix_list[index] == "mu" and infix_list[index+1] != "(":
                vtemp.append(element)
                vtemp.append("(")
                stemp.append("mu")
            elif element == "(":
                vtemp.append(element)
                stemp.append("ord")
            elif self.is_binary_operator(element) and len(stemp) > 0 and stemp[-1] == "mu":
                while len(stemp) > 0 and stemp[-1] == "mu":
                    vtemp.append(")")
                    stemp.pop()

                vtemp.append(element)
            elif element == ")" and len(stemp) > 0 and stemp[-1] == "ord":
                vtemp.append(element)
                stemp.pop()
                while (len(stemp) > 0 and stemp[-1] == "mu"):
                    vtemp.append(")")
                    stemp.pop()
            else:
                vtemp.append(element)

        while len(stemp) > 0:
            if (stemp[-1] == "mu"):
                vtemp.append(")")
            stemp.pop()

        infix_list = vtemp

        return infix_list

    # Create a postfix list from an infix list
    def create_postfix_list(self, infix_list):
        postfix_list = []  # Set up local postfix list
        operator_stack = []  # Set up operator stack (Actually a list treated as a stack)
        
        for index, element in enumerate(infix_list):
            if not self.is_operator(element):
                postfix_list.append(element)  # If the element is not an operator then add it to the postfix list
            else:
                if len(operator_stack) == 0:
                    operator_stack.append(element)
                elif element == "(":
                    operator_stack.append(element)
                elif self.precedence_level(element) > self.precedence_level(operator_stack[-1]):
                    operator_stack.append(element)
                elif element == ")":
                    while operator_stack[-1] != "(":    # Pop all the stack operators until "("
                        postfix_list.append(operator_stack[-1])
                        operator_stack.pop()
                    operator_stack.pop()  # Pop the '(' operator
                else:
                    while len(operator_stack) > 0 and operator_stack[-1] != "(" and self.precedence_level(operator_stack[-1]) >= self.precedence_level(element):
                        postfix_list.append(operator_stack[-1])
                        operator_stack.pop()

                    operator_stack.append(element)

        while len(operator_stack) > 0:
            postfix_list.append(operator_stack[-1])
            operator_stack.pop()

        return postfix_list
    
    # Returns a number (0-4) indictating precedence level for the operator
    def precedence_level(self, operator):
        if operator == "(" or operator == ")":
            return 0
        elif operator == "+" or operator == "-":
            return 1
        elif operator == "^":
            return 3
        elif operator == "sin" or operator == "cos" or operator == "tan" or operator == "sqrt" or operator == "mu":
            return 4
        else:
            return 2

    def get_infix_list(self):
        return self.infix_list
    
    def get_postfix_list(self):
        return self.postfix_list

    # Tests is the string token is in the operator list (and therefore a legit operator)
    def is_operator(self, token):
        return token in self.operator_list
    
    # Tests if operator used on 1 operand (unary operator)
    def is_unary_operator(self, token):
        result = False

        match token:
            case "sin" | "cos" | "tan" | "sqrt" | "mu":
                result = True
            case _:
                result = False

        return result                


    # Tests if operator requires 2 operands (binary operator)
    def is_binary_operator(self, token):
        result = False

        match token:
            case "^" | "*" | "/" | "+" | "-":
                result = True
            case _:
                result = False

        return result        

    # If its not an operator then it must be an operand (number or string representation of a variable)
    def is_number_or_variable(self, token):
        return not self.is_operator(token)

    # Remove any whitespace from the expression string up front.
    def remove_whitespace(self, expression):
        return expression.replace(" ", "")

    # Chceks if the string expression is properly formatted, otherwise raise an exception
    def check_syntax(self, infix_list):
        brackets = []

        # If the infix list is empty, then nothing to check
        if len(infix_list) == 0:
            raise SyntaxError(infix_list, 0, ErrorType.Zero_Length_Expression)
        
        for index, element in enumerate(infix_list):
            if index == 0:
                if element == ")" or element == "*" or element == "/" or element == "+" or element == "^":
                    raise SyntaxError(infix_list, index, ErrorType.Invalid_Character)
                elif element == "(":
                    brackets.append(index)
            elif index > 0:
                if element == "(":
                    if self.is_number_or_variable(infix_list[index-1]) or infix_list[index-1] == ")":
                        raise SyntaxError(infix_list, index, ErrorType.Invalid_Character)
                    brackets.append(index)
                elif element == "-":
                    if self.is_unary_operator(infix_list[index-1]):
                        raise SyntaxError(infix_list, index, ErrorType.Invalid_Character)
                elif self.is_binary_operator(element):
                    if infix_list[index-1] == "-" or self.is_unary_operator(infix_list[index-1]) or infix_list[index-1] == "(" or self.is_binary_operator(infix_list[index-1]):
                        raise SyntaxError(infix_list, index, ErrorType.Invalid_Character)
                elif self.is_unary_operator(element):
                    if infix_list[index-1] == ")" or self.is_unary_operator(infix_list[index-1]) or self.is_number_or_variable(infix_list[index-1]):
                        raise SyntaxError(infix_list, index, ErrorType.Invalid_Character)
                elif self.is_number_or_variable(element):
                    if infix_list[index-1] == ")" or self.is_unary_operator(infix_list[index-1]) or self.is_number_or_variable(infix_list[index-1]):
                        raise SyntaxError(infix_list, index, ErrorType.Invalid_Character)
                elif element == ")":
                    if infix_list[index-1] == "(" or self.is_binary_operator(infix_list[index-1]) or self.is_unary_operator(infix_list[index-1]) or len(brackets) <= 0:
                        raise SyntaxError(infix_list, index, ErrorType.Invalid_Character)
                    brackets.pop()

        last = len(infix_list) - 1  # Assigning the last index

        if self.is_unary_operator(infix_list[last]) or self.is_binary_operator(infix_list[last]) or infix_list[last] == "(":
            raise SyntaxError(infix_list, index, ErrorType.Invalid_Character)
        elif len(brackets) > 0:
            raise SyntaxError(infix_list, index, ErrorType.Missing_Parentheses)
        else:
            return True
    