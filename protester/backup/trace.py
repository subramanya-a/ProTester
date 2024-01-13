import traceback
import inspect
import re
import os
import sys
import linecache

# Enable ANSI escape codes for color on Windows
os.system("")



def test_case():
    a= 5
    c=a
    if 1 == 1:
        b=c
    assert (1 * 5) == 1


def Print_exception():
    try:
        test_case()
    except Exception as exc:


        # exception_type, exception_object, exception_traceback = sys.exc_info()
        # filename = exception_traceback.tb_frame.f_code.co_filename
        # line_number = exception_traceback.tb_lineno
        # print("Exception type: ", exception_type)
        # print("File name: ", filename)
        # print("Line number: ", line_number)
        
        # print( 'line', inspect.getframeinfo(inspect.currentframe()).lineno, 
        #     'of file', inspect.getframeinfo(inspect.currentframe()).filename )

        # frame_info = inspect.getframeinfo(inspect.currentframe())
        # function_name = inspect.currentframe().f_code.co_name
        # print(f"Error in function '{function_name}' at line {frame_info.lineno}")



        tb = traceback.extract_tb(exc.__traceback__)
        if tb:
            last_frame = tb[-1]
            file_name, line_number, func_name, _ = last_frame
            print(f"Error in function '{func_name}' at line {line_number}")
        else:
            print("Failed to extract last frame information.")
        
        # print(traceback.format_exc())
        
        # Get the code snippet around the failure line using linecache
        snippet_start = max(1, line_number - 5) # 5 previous code 
        snippet_end = line_number + 1 #min(line_number + 2, len(linecache.getlines(file_name)) + 1)
        # relevant_code = []
        # for i in range(9, snippet_end):
        #     line_code =  linecache.getline(file_name, i)
        #     if line_code != "\n":
        #         relevant_code.append(line_code)
        relevant_code = [linecache.getline(file_name, i) for i in range(snippet_start, snippet_end) if linecache.getline(file_name, i).strip()]


        # Highlight the error line (assert) in red
        assert_line = relevant_code[-1]
        highlighted_assert_line = f"\033[91m{assert_line}\033[0m"
        underline = f"\033[91m{' ' * (len(assert_line) - len(assert_line.lstrip()))}{'^' * len(assert_line.lstrip())}\033[0m"

        # Print the formatted code snippet with the failure line marked
        print(f"""
        Failed: {exc}
        Code snippet around the failure line:
        {''.join(relevant_code[:-1])}
        {highlighted_assert_line}
        {underline}
        """)




        # # Get the formatted traceback as a string
        # tb_str = traceback.format_exc().strip()
    #     # Use a regular expression to extract the line number
    #     match = re.search(r'File ".+", line (\d+),', tb_str)
    #     if match:
    #         line_number = int(match.group(1))
    #     else:
    #         print("Failed to extract line number from the traceback.")
    #         print("Traceback:", tb_str)
    #         line_number = 0  # Set a default value

    #     # Get the code snippet around the failure line
    #     code_snippet = inspect.getsource(test_case).split("\n")

    #     if 0 <= line_number < len(code_snippet):
    #         snippet_start = max(0, line_number - 3)
    #         snippet_end = min(len(code_snippet), line_number + 2)
    #         relevant_code = code_snippet[snippet_start:snippet_end]

    #         # Highlight the error line in red
    #         highlighted_line = f"\033[91m{code_snippet[line_number - 1].rstrip()}\033[0m"

    #         # Print the formatted code snippet with the failure line marked
    #         print(f"""
    # Code snippet around the failure line:
    # {''.join(relevant_code).rstrip()}

    # Failed: {exc}
    # {highlighted_line}

    # {tb_str}
    # """)
    #     else:
    #         print("Error: Line number is out of range.")

Print_exception()