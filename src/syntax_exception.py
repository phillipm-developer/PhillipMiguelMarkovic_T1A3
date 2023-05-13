from enum import Enum

# Using enumerated type to indicate syntax error types
class SyntaxErrorType(Enum):
    Invalid_Character = 1
    Missing_Parentheses = 2
    Zero_Length_Expression = 3

# Custom SyntaxError exception. Puts together an expressive error message.
class SyntaxError(Exception):
    def __init__(self, infix_list, index, error_type):  # The index parameter specifies which element is at fault
        self.infix_list = infix_list
        self.error_message = ""
        self.equation = ""
        self.arrow = ""
        self.index = index

        match error_type:
            case SyntaxErrorType.Invalid_Character:
                self.error_message += f"Error at column {self.index+1} in "
                self.get_arrow()
                self.error_message += self.equation
                self.error_message += self.arrow
            
            case SyntaxErrorType.Missing_Parentheses:
                self.error_message += f"Missing closing bracket at column {self.index+1} in "
                self.get_arrow()
                self.error_message += self.equation
                self.error_message += self.arrow

            case SyntaxErrorType.Zero_Length_Expression:
                self.error_message = "Zero length expression - Nothing to evaluate."

            case _:
                pass

    # Creates & returns a carrot with precisely calculated trailing spaces
    # to indicate which element is misplaced in the expression. It appears below 
    # the error message
    def get_arrow(self):
        new_index = 0
        exp = ""
    
        for index, element in enumerate(self.infix_list):
           exp += element
           if (index == self.index):
                new_index = len(exp) - 1

        self.equation = exp

        new_index = len(self.error_message) + new_index
        for i in range(new_index):
            self.arrow += " "
        self.arrow += "^"
        self.arrow = "\n" + self.arrow

    def get_message(self):
        return self.error_message
     