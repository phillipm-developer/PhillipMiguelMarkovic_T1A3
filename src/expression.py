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
        self.remove_whitespace(self.expression)
        self.values_set = False
        self.assign_infix_list(self.expression)

    # End-user readable representation of the object
    def __str__(self):
        return self.expression

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
        # if not self.check_syntax(self.infix_list):
        #     return


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

    def get_infix_list(self):
        return self.infix_list
    
    def assign_postfix_list(self):
        pass

    def is_operator(self, token):
        return token in self.operator_list
    
    def is_unary_operator(self, token):
        pass

    def is_binary_operator(self, token):
        result = False

        match token:
            case "^" | "*" | "/" | "+" | "-":
                result = True
            case _:
                result = False

        return result        


    def is_number_or_variable(self, token):
        pass

    def remove_whitespace(self, expression):
        self.expression = expression.replace(" ", "")

    def check_syntax(self, infix_list):
        pass