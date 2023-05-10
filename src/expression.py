import math_exception
import syntax_exception
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
        self.remove_whitespace(self.expression)
        self.assign_infix_list(self.expression)
        self.assign_postfix_list()

    # Allows same instance of Expression to be used with a new function
    def parse_expression(self, expression):
        if len(self.infix_list) > 0:
            self.infix_list = []
        if len(self.postfix_list) > 0:
            self.postfix_list = []

        self.expression = expression
        
        # Re-initialise the expression
        self.values_set = False
        self.remove_whitespace(self.expression)
        self.assign_infix_list(self.expression)
        self.assign_postfix_list()

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
    # in a list of equivalent size
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
        for key, value in substitutions.items():
            for index, element in enumerate(self.postfix_list):
                if element == key:
                    self.postfix_list[index] = value
        result = self.evaluate(postfix_list)
        calculation_dict['result'] = result
        calculation_dict['solved'] = True
        return calculation_dict


    # Evaluates the postfix list
    def evaluate(self, postfix_list):
        operand_stack = []
        result = 0

        for index, element in enumerate(postfix_list):
            if not self.is_operator(element):
                operand_stack.append(float(element))
            else:
                match element:
                    case "+":
                        op2 = operand_stack[-1]
                        operand_stack.pop()
                        op1 = operand_stack[-1]
                        operand_stack.pop()
                        temp = op1 + op2
                        operand_stack.append(temp)

                    case "-":
                        op2 = operand_stack[-1]
                        operand_stack.pop()
                        op1 = operand_stack[-1]
                        operand_stack.pop()
                        temp = op1 - op2
                        operand_stack.append(temp)

                    case "*":
                        op2 = operand_stack[-1]
                        operand_stack.pop()
                        op1 = operand_stack[-1]
                        operand_stack.pop()
                        temp = op1 * op2
                        operand_stack.append(temp)

                    case "/":
                        op2 = operand_stack[-1]
                        operand_stack.pop()
                        op1 = operand_stack[-1]
                        operand_stack.pop()

                        if op2 == 0:
                            raise math_exception.MathException(math_exception.ErrorType.Divide_By_Zero)
                        
                        temp = op1 / op2
                        operand_stack.append(temp)

                    case "^":
                        op2 = operand_stack[-1]
                        operand_stack.pop()
                        op1 = operand_stack[-1]
                        operand_stack.pop()
                        temp = pow(op1, op2)
                        operand_stack.append(temp)

                    case "sin":
                        op1 = operand_stack[-1]
                        operand_stack.pop()
                        temp = math.sin(op1)
                        operand_stack.append(temp)

                    case "cos":
                        op1 = operand_stack[-1]
                        operand_stack.pop()
                        temp = math.cos(op1)
                        operand_stack.append(temp)

                    case "tan":
                        op1 = operand_stack[-1]
                        operand_stack.pop()
                        temp = math.tan(op1)
                        operand_stack.append(temp)

                    case "sqrt":
                        op1 = operand_stack[-1]
                        operand_stack.pop()
                        temp = math.sqrt(op1)
                        operand_stack.append(temp)

                    case "mu":
                        op1 = operand_stack[-1]
                        operand_stack.pop()
                        temp = -1 * op1
                        operand_stack.append(temp)

        result = operand_stack[-1]
        return result
    
    # Converts the expression to infix form for later use
    def assign_infix_list(self, infix_string):
        token = ''  # Appended to character by character to form a string
        for element in infix_string:
            if self.is_operator(element):
                if len(token) > 0:
                    self.infix_list.append(token)
                    token = ''

                self.infix_list.append(element)
            else:
                token += element

        if len(token) > 0:
            self.infix_list.append(token)
            token = ''

        # Check that the expression is properly formed
        if not self.check_syntax(self.infix_list):
            return


        # Insert unary minus operators
        for index, element in enumerate(self.infix_list):
            if element == "-":
                if index == 0:
                    self.infix_list[index] = "mu"
                elif index > 0 and index < len(self.infix_list)-1 and self.is_operator(self.infix_list[index-1]) and self.infix_list[index-1] != ")":
                    self.infix_list[index] = "mu"

        # Insert parentheses to encompass the operand for a unary minus operator. A unary minus is treated as a 
        # function the way sin & cos are as they only apply to a single operator as well

        stemp = []  # We treat this variable as a stack
        vtemp = []  # We construct the new list consisting of expression tokens with the parentheses inserted for unary minus (mu)

        for index, element in enumerate(self.infix_list):
            if self.infix_list[index] == "mu" and self.infix_list[index+1] != "(":
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

        self.infix_list = vtemp

        return self.infix_list

    # Convert from infix to postfix form and store in posfix_list
    def assign_postfix_list(self):
        operator_stack = []

        for index, element in enumerate(self.infix_list):
            if not self.is_operator(element):
                self.postfix_list.append(element)
            else:
                if len(operator_stack) == 0:
                    operator_stack.append(element)
                elif element == "(":
                    operator_stack.append(element)
                elif self.precedence_level(element) > self.precedence_level(operator_stack[-1]):
                    operator_stack.append(element)
                elif element == ")":
                    while operator_stack[-1] != "(":    # Pop all the stack operators until "("
                        self.postfix_list.append(operator_stack[-1])
                        operator_stack.pop()
                    operator_stack.pop()  # Pop the '(' operator
                else:
                    while len(operator_stack) > 0 and operator_stack[-1] != "(" and self.precedence_level(operator_stack[-1]) >= self.precedence_level(element):
                        self.postfix_list.append(operator_stack[-1])
                        operator_stack.pop()

                    operator_stack.append(element)

        while len(operator_stack) > 0:
            self.postfix_list.append(operator_stack[-1])
            operator_stack.pop()

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
        self.expression = expression.replace(" ", "")
        return self.expression

    # Chceks if the string expression is properly formatted, otherwise raise an exception
    def check_syntax(self, infix_list):
        brackets = []

        for index, element in enumerate(infix_list):
            if index == 0:
                if element == ")" or element == "*" or element == "/" or element == "+" or element == "^":
                    raise syntax_exception.SyntaxException(infix_list, index, syntax_exception.ErrorType.Invalid_Character)
                elif element == "(":
                    brackets.append(index)
            elif index > 0:
                if element == "(":
                    if self.is_number_or_variable(infix_list[index-1]) or infix_list[index-1] == ")":
                        raise syntax_exception.SyntaxException(infix_list, index, syntax_exception.ErrorType.Invalid_Character)
                    brackets.append(index)
                elif element == "-":
                    if self.is_unary_operator(infix_list[index-1]):
                        raise syntax_exception.SyntaxException(infix_list, index, syntax_exception.ErrorType.Invalid_Character)
                elif self.is_binary_operator(element):
                    if infix_list[index-1] == "-" or self.is_unary_operator(infix_list[index-1]) or infix_list[index-1] == "(" or self.is_binary_operator(infix_list[index-1]):
                        raise syntax_exception.SyntaxException(infix_list, index, syntax_exception.ErrorType.Invalid_Character)
                elif self.is_unary_operator(element):
                    if infix_list[index-1] == ")" or self.is_unary_operator(infix_list[index-1]) or self.is_number_or_variable(infix_list[index-1]):
                        raise syntax_exception.SyntaxException(infix_list, index, syntax_exception.ErrorType.Invalid_Character)
                elif self.is_number_or_variable(element):
                    if infix_list[index-1] == ")" or self.is_unary_operator(infix_list[index-1]) or self.is_number_or_variable(infix_list[index-1]):
                        raise syntax_exception.SyntaxException(infix_list, index, syntax_exception.ErrorType.Invalid_Character)
                elif element == ")":
                    if infix_list[index-1] == "(" or self.is_binary_operator(infix_list[index-1]) or self.is_unary_operator(infix_list[index-1]) or len(brackets) <= 0:
                        raise syntax_exception.SyntaxException(infix_list, index, syntax_exception.ErrorType.Invalid_Character)
                    brackets.pop()

        last = len(infix_list) - 1  # Assigning the last index

        if self.is_unary_operator(infix_list[last]) or self.is_binary_operator(infix_list[last]) or infix_list[last] == "(":
            raise syntax_exception.SyntaxException(infix_list, index, syntax_exception.ErrorType.Invalid_Character)
        elif len(brackets) > 0:
            raise syntax_exception.SyntaxException(infix_list, index, syntax_exception.ErrorType.Missing_Parentheses)
        else:
            return True
    