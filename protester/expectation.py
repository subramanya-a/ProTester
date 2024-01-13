import operator

def expect(value):
    return Expectation(value)

class FailedExpectationError(RuntimeError):
    def __init__(self, message):
        self.message = message

class Expectation:
    def __init__(self, value):
        self.value = value

    def toEqual(self, comparison):
        self._assert(comparison, operator.eq, "to equal")

    def notToEqual(self, comparison):
        self._assert(comparison, operator.is_not, "not to equal")

    def toInclude(self, element):
        self._assert(element, operator.contains, "to include")

    def notToInclude(self, element):
        def not_include(ls, el):
            return el not in ls
        self._assert(element, not_include, "not to include")

    def _assert(self, comparison, op, message):
        if not op(self.value, comparison):
            raise FailedExpectationError(f"expected {self.value} {message} {comparison}")


import linecache
import sys
import traceback

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print( 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

# def LogException(exc):
#     exc_type, exc_obj, tb = sys.exc_info()
#     tb = traceback.extract_tb(exc.__traceback__)
#     if tb:
#         last_frame = tb[-1]
#         file_name, line_number, func_name, _ = last_frame
#         # print(f"Error in function '[{file_name}]{func_name}:{line_number}")
    
#         if exc_type is AssertionError:
#             return ('AssertionError IN ({}, LINE {} {}): {}'.format(file_name, line_number, func_name, exc))
#         else :
#             return exc #('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(file_name, line_number, func_name, exc))
#     else:
#         print("Failed to extract last frame information.")

def LogException(exc):
    try:
        exc_type, exc_obj, tb = sys.exc_info()
        traceback_info = traceback.extract_tb(exc.__traceback__)

        if traceback_info:
            last_frame = traceback_info[-1]
            file_name, line_number, func_name, _ = last_frame
            print(f"Error in function '{func_name}' at line {line_number}")
        else:
            print("Failed to extract last frame information.")
            return None  # Return None if traceback information is not available

        # Get the code snippet around the failure line using linecache
        snippet_start = max(1, line_number - 5)  # 5 previous code
        snippet_end = line_number + 1

        relevant_code = [linecache.getline(file_name, i).strip() for i in range(snippet_start, snippet_end)]

        # Highlight the error line (assert) in red
        assert_line = relevant_code[-1]
        highlighted_assert_line = f"{assert_line}"

        # Print the formatted code snippet with the failure line marked
        return {
            "excp_type": exc_type.__name__,
            "file": file_name,
            "line": line_number,
            "func": func_name,
            "assert_code": highlighted_assert_line,
        }
    except Exception as e:
        print(f"Error in LogException: {e}")
        return None  # Return None in case of an error

# tests/test_basic.py LINE 8 test_failure[parameters]