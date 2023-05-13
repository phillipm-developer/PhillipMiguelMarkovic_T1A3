from enum import Enum

# Using enumerated type to indicate syntax error types
class MathErrorType(Enum):
    Divide_By_Zero = 1
    Values_Not_Set = 2
    More_Than_One_Variable = 3

# Custom SyntaxError exception. Puts together an expressive error message.
class MathError(Exception):
    def __init__(self, error_type):
        self.error_message = ""

        match error_type:
            case MathErrorType.Divide_By_Zero:
                self.error_message = "Attempted to divide by zero"
            case MathErrorType.Values_Not_Set:
                self.error_message = "Not all variables have been set"
            case MathErrorType.More_Than_One_Variable:
                self.error_message = "Not permitted more than one variable"

    def get_message(self):
        return self.error_message
