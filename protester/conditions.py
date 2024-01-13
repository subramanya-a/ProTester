import types
from . TestCaseCollections import protester_collections
verbose_func = protester_collections.verbose

def is_lambda(func):
    return isinstance(func, types.LambdaType)

def is_teststatus(suite_name_s, testcase_name_s):
    test_suites = protester_collections.get_testsuites()
    try:
        for testsuite in test_suites:
            suite_name = testsuite.attributes.get('name', '')
            
            if suite_name_s is not None:
                if suite_name_s != suite_name:
                    continue # skip for for next index

            for testcase in testsuite.get_testcases():
                testcase_name = testcase.attributes.get('name', '')
                if testcase_name_s is not None:
                    # check test case name is available
                    if testcase_name_s == testcase_name:
                        # get the result for the testcase
                        result  = testcase.attributes.get('result', {"status":False, "detail":"default detail"})
                        
                        return result["status"]
    except Exception as e:
        print(e)
        
    return None

def split_suite_func(suite_func):
    suitename, function_name = None, None  # Initialize suitename and function_name
    try:
        parts = suite_func.split("::", 1)
        if len(parts) == 2:
            suitename, function_name = parts
        else:
            suitename = None
            function_name = parts[0]
    except Exception as e:
        print(e)

    return suitename, function_name


def is_pass(func:str):
    suitename, function_name = split_suite_func(func)
    result =  is_teststatus(suitename, function_name)
    
    if result is None:
        return False, f"Test Case:{func} not found"

    # if test is not excuted, inform the user to update the detail to order the testcase
    if result == verbose_func("NX"):
        return True, f"Test case {func} is not executed, ordering the testcase needs an update."
        
    # if test executed and result is pass return true
    if result in [verbose_func("P")]:
        return True, f"Test Case:{func} got Passed"
    # Test case failed or skipped
    return False, f"Test Case:{func} got Failed, hence Skipping the execution"

    
def is_fail(func):
    suitename, function_name = split_suite_func(func)
    result =  is_teststatus(suitename, function_name)
    
    if result is None:
        return False, f"Test Case:{func} not found"

    # if test is not excuted, inform the user to update the detail to order the testcase
    if result == verbose_func("NX"):
        return True, f"Test case {func} is not executed, ordering the testcase needs an update."
        
    # if test executed and result is pass return true
    if result in [verbose_func("F")]:
        return True, f"Test Case:{func} got Failed"

    # Test case failed or skipped
    return False, f"Test Case:{func} got Passed, hence Skipping the execution"
   