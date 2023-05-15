# Imports the sys module and a custom logging module from the src package
import sys
from src.logger import logging

# This function takes an error object and a sys object as input, extracts information about the error, and returns it as a string
def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name: [{0}] line number: [{1}] error message: [{2}]".format(file_name, exc_tb.tb_lineno, str(error))
    return error_message

# This class defines a custom exception that inherits from the built-in Exception class
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message

# This block of code attempts to divide 1 by 0 in a try block, which will raise a ZeroDivisionError exception
if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        # This line logs a message using the custom logging module
        logging.info("Divide by zero error")
        # This line raises an instance of the CustomException class, passing the caught exception object and the sys module as arguments
        raise CustomException(e, sys)
