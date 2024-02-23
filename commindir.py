import inspect

def get_call_info():
    frame = inspect.currentframe().f_back
    line_number = frame.f_lineno
    function_name = frame.f_code.co_name
    return f"Called from {function_name} on line {line_number}"

# Example usage
def some_function():
    print(get_call_info())

some_function()