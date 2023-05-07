from enum import Enum

class ErrorType(Enum):
    Divide_By_Zero = 1
    Values_Not_Set = 2

class MathException(Exception):
    def __init__(self, infix_list, index, error_type):
        self.error_message = ""

        match error_type:
            case ErrorType.Divide_By_Zero:
                self.error_message = "Attempted to divide by zero"
            case ErrorType.Values_Not_Set:
                self.error_message = "Not all variables have been set"

    def get_message(self):
        return self.error_message
