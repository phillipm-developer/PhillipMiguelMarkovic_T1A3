from enum import Enum

class ErrorType(Enum):
    Invalid_Character = 1
    Missing_Parentheses = 2
    Zero_Length_Expression = 3

class SyntaxError(Exception):
    def __init__(self, infix_list, index, error_type):
        self.infix_list = infix_list
        self.error_message = ""
        self.equation = ""
        self.arrow = ""
        self.index = index

        match error_type:
            case ErrorType.Invalid_Character:
                self.error_message += f"Error at column {self.index+1} in "
                self.get_arrow()
                self.error_message += self.equation
                self.error_message += self.arrow
            
            case ErrorType.Missing_Parentheses:
                self.error_message += f"Missing closing bracket at column {self.index+1} in "
                self.get_arrow()
                self.error_message += self.equation
                self.error_message += self.arrow

            case ErrorType.Zero_Length_Expression:
                self.error_message = "Zero length expression - Nothing to evaluate."

            case _:
                pass

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
     