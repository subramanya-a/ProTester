import importlib.machinery
import types
from inspect import getmembers, isfunction
import sys
import os
from . import colors
from .expectation import LogException
from inspect import isfunction, ismethod,isclass, getmembers
from . TestCaseCollections import protester_collections, TestSuiteCollection, TestCaseCollection, Info
from jinja2 import Environment, FileSystemLoader
from protester.conditions import is_lambda
import getpass
import sys
# add the path of working directory to the the sys path
sys.path.append(os.getcwd())


def calculate_ratio(numerator, denominator):
    """
    Calculate the ratio of numerator to the denominator.
    Returns the calculated ratio.
    """
    if denominator != 0:
        return f"{(numerator / denominator) * 100:.2f}" 
    else:
        return f"{0 * 100:.2f}" 

class Runner:
    def __init__(self, path):
        self.protester_collections = protester_collections
        self.test_suite_ungrouped = None 
        self.path = os.path.join(os.getcwd(),path)
        self.test_files = []
        self.successes, self.failures = 0, 0
        self.not_x, self.skipped_x = 0, 0
        self.load_test_files(self.path)

    def is_test_file(self, file_name):
        return file_name.endswith("_test.py") or file_name.startswith("test_")

    def load_test_files(self, path):
        if path.endswith(("__pycache__","html")):
            return
        
        # list the function only if the file has python extension and is test file
        # if os.path.isfile(path) and path.endswith(".py") and self.is_test_file(os.path.basename(path)):
        if os.path.isfile(path) and path.endswith(".py"): # protester hooks can be in any file, so test_*.py or *_test.py checks are removed
            self.test_files.append(path)
        
        elif os.path.isdir(path):
            # Add the directory path to sys.path
            sys.path.append(path)

            for nested_path in os.listdir(path):
                self.load_test_files(path + "/" + nested_path)

    def load_tests(self, mod):
        # return [m for m in getmembers(mod) if isfunction(m[1]) and m[0].startswith("test_")]

        for name, obj in getmembers(mod):
            if isclass(obj) and name.startswith("TEST"):
                test_suite = TestSuiteCollection()
                class_methods = getmembers(obj, predicate=isfunction)
                category_name = f"{name}"

                """collect the class / function decorators info"""
                test_suite.set_attributes(category_name, obj, doc=obj.__doc__)

                # if category_name not in self.grouped_tests:
                #     self.grouped_tests[category_name] = []

                for method_name, method_obj in class_methods:
                    if method_name.startswith("test_"):
                        testcase = TestCaseCollection()
                        testcase.set_attributes(method_name, method_obj, doc=method_obj.__doc__)
                        test_suite.add_testcase(testcase)
                    elif method_name.startswith("protester_"):
                        self.protester_collections.pro_tester_modules.append({"name":method_name, "func":method_name})
                    else :
                        pass
                
                # Order the test cases by name/sequence
                test_suite.order_testcases()

                self.protester_collections.add_testsuite(test_suite)

            elif isfunction(obj) and name.startswith("test_"):
                # if none create the group here
                if self.test_suite_ungrouped is None:
                    self.test_suite_ungrouped = TestSuiteCollection()   # Ensure 'ungrouped' key exists common to testcase to all files        
                    self.test_suite_ungrouped.set_attributes("ungrouped", None)
        
                
                function_id = getattr(obj, 'testcase', None)
                function_description = getattr(obj, 'description', None)
                function_extra_tags = getattr(obj, 'extra_tags', None)

                print(f"{name} ID: {function_id}, Description: {function_description}, Extra Tags: {function_extra_tags}")

                testcase = TestCaseCollection()
                testcase.set_attributes(name, obj, doc=obj.__doc__)
                self.test_suite_ungrouped.add_testcase(testcase)
            elif isfunction(obj) and name.startswith("protester_"):
                self.protester_collections.pro_tester_modules.append({"name":name, "func":obj})
            else :
                pass

    def load_module(self, file):
        loader = importlib.machinery.SourceFileLoader("testmod", file)
        mod = types.ModuleType("testmod")
        loader.exec_module(mod)
        return mod
    
    def generate_report(self,overall_result, test_info, statistics):
        env = Environment(auto_reload=False)
        path = os.path.join(os.path.dirname(__file__), 'report')
        env.loader = FileSystemLoader(path)
        
        # Create Jinja2 environment
        # env = Environment(loader=FileSystemLoader("report"))

        # Define Jinja2 template
        template = env.get_template("template.html")


        # Get the current Windows username
        username = getpass.getuser()

        sut_configs = Info()
        sut_configs_inst = sut_configs.add_header("Test Engineer")
        sut_configs_inst.add_table_item("Windows Login Name: ", f"{username}")

        sut_infos = Info()

        # Render template with data
        output_html = template.render(test_suites=self.protester_collections.testsuites,
                                    test_info=test_info, statistics=statistics,
                                    title=self.protester_collections.execute_protester_function("protester_report_title", "Pro Tester"),
                                    sut_configs=self.protester_collections.execute_protester_function("protester_sut_config", [],params={"items":sut_configs}),
                                    sut_infos=self.protester_collections.execute_protester_function("protester_sut_info", [],params={"items":sut_infos}),
                                    overall_result=overall_result)

        # Write HTML to a file
        # with open("output.html", "w") as file:
        file_path = os.path.join(self.path, './', 'report/report.html')

        # Ensure the directory exists before opening the file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(output_html)

    def perform_test(self, test_name, test_function, args): 
        
        # # Accessing attributes in the runner
        # function_id = getattr(test_function, 'testcase', None)
        # function_description = getattr(test_function, 'description', None)
        # function_extra_tags = getattr(test_function, 'extra_tags', None)

        # print(f"ID: {function_id}, Description: {function_description}, Extra Tags: {function_extra_tags}")
        
        try:
            test_function(protest=args)
            self.successes += 1
            print(f"{test_name} - success")
            return True, ""
        except AssertionError as msg:
            print(f"{colors.RED}{test_name} - failure{colors.RESET}")
            print(f"{colors.RED}    Reason: {LogException(msg)}{colors.RESET}")
            self.failures += 1
            return False, LogException(msg)
        except Exception as e:
            print(f"{colors.RED}{test_name} - failure{colors.RESET}")
            print(f"{colors.RED}    Reason: {LogException(e)}{colors.RESET}")
            self.failures += 1
            return False, LogException(e)
 
    def dependency_check(self,item, params,**kwargs):
        """
        This method checks the dependency and returns the appropriate result.
        Returns True if the test case dependency is okay to execute, False otherwise.
        Input:
        item : test suite or case 
        """
        # Step 1: Check if variant is supported
        variants = item.attributes.get("variants", None)
        # check if the variants is available, and not empty
        # if variants is not None:
        if variants:
            status, message = protester_collections.execute_protester_function("protester_is_variant_supported",(True,"Default supported!"),
                                        params={"variants":variants})
            if not status:
                item.update_attribute("result",
                                        {
                                            "status": item.verbose("SX"),
                                            "detail": message
                                        })
                self.not_x += 1 
                return False

        # Step 2: Check skip conditions
        skipif_conditions =item.attributes.get("skipif", [])
        skipif_results = []
        message = "no reason provided by tester"
        #  check the condition, if the conditions is not none  
        # if skipif_conditions is not None and len(skipif_conditions) > 0:
        if skipif_conditions:
            for index, condition in enumerate(skipif_conditions):            
                try:
                    if is_lambda(condition):
                        print(f"Lambda function: {condition}")
                        status, message = condition(**params)
                    elif callable(condition):
                        print(f"Regular function: {condition.__name__}")
                        status, message = condition(**params)
                    else:
                        print("Non-callable element in skip conditions.")
                        status, message = condition
                    
                    # By default if the function has no return status allow the execution, instead of blocking
                    skipif_results.append(bool(status) if status is not None else False)

                    if message is None or message == "":
                        message = "no reason provided by tester"
                    
                    if status:
                        print(f"Skipping due to condition({index}): {message}")
                        # set the reason and break the loop for other condition
                        break
                except Exception as e:
                    print(f"Error at index {index}: {e}")
                    item.update_attribute("result", {"status": item.verbose("F"), "detail": e})
                    return False
            
            if any(skipif_results):
                print(f"Skipping due to skip conditions {message}")
                item.update_attribute("result",
                                        {
                                            "status": item.verbose("S"),
                                            "detail": message
                                        })
                self.skipped_x += 1
                return False
        
        # # Step 3: Check execute conditions
        executeif_conditions =item.attributes.get("executeif", [])
        executeif_results = []
        message = "no reason provided by tester"

        #  check the condition, if the conditions is not none  
        # if executeif_conditions is not None and len(executeif_conditions) > 0:
        if executeif_conditions:
            for index, condition in enumerate(executeif_conditions):            
                try:
                    if is_lambda(condition):
                        print(f"Lambda function: {condition}")
                        status, message = condition(**params)
                    elif callable(condition):
                        print(f"Regular function: {condition.__name__}")
                        status, message = condition(**params)
                    else:
                        print("Non-callable element in xskip conditions.")
                        status, message = condition

                    print(status, message)
                    # By default if the function has no return status allow the execution, instead of blocking
                    executeif_results.append(bool(status) if status is not None else False)

                    if message is None or message == "":
                        message = "no reason provided by tester"

                    if status:
                        print(f"execute Skipped due to condition({index}): {message}")
                        # set the reason and break the loop for other condition
                        break
                except Exception as e:
                    print(f"Error at index {index}: {e}")
                    item.update_attribute("result", {"status": item.verbose("F"), "detail": LogException(e)})
                    return False
            
            if any(executeif_results): 
                # execute if any one is true
                print(f"execute Skipped due to skip conditions")
                item.update_attribute("result",
                                        {
                                            "status": item.verbose("SX"),
                                            "detail": message
                                        })
                self.not_x += 1 
                return False
        
        # above negative case are covered, if reaching here should be positive
        return True
    
    def execute_test(self,testcase, params, kwargs ):

        # check for the dependency, execute only if true
        if self.dependency_check(testcase, params,**kwargs ):
            # check the pre-execution conditions 
            pre_func = testcase.attributes.get("pre", None)
            if callable(pre_func): pre_func()

            func = testcase.attributes.get("func", lambda: None)
            func_name = testcase.attributes.get("name", "")
            try:
                func(protest=testcase, **params, **kwargs)
                # Pass the patched parameters and scenario name to the function
                # with patch.dict('__main__.__dict__', {"TS_NAME": scenario_name}):
                #     # result = func(*args, parameters=params, **kwargs)
                #     result = func(*args, **params, **kwargs)
                    
                self.successes += 1
                print(f"{func_name} - success")
                status , result = True , ""
            except AssertionError as msg:
                print(f"{colors.RED}{func_name} - failure{colors.RESET}")
                print(f"{colors.RED}    Reason: {LogException(msg)}{colors.RESET}")
                self.failures += 1
                status , result = False, LogException(msg)
            except Exception as e:
                print(f"{colors.RED}{func_name} - failure{colors.RESET}")
                print(f"{colors.RED}    Reason: {LogException(e)}{colors.RESET}")
                self.failures += 1
                status , result = False, LogException(e)

                print(e)
    
            if status:
                testcase.update_attribute("result", {"status": testcase.verbose("P"), "detail": result})
            else: 
                testcase.update_attribute("result", {"status": testcase.verbose("F"), "detail": result})

            # check the post-execution conditions 
            post_func = testcase.attributes.get("post", None)
            if callable(post_func): post_func()

            logger = testcase.attributes.get("steps", None)
            # if (logger is not None) and (testcase.attributes.get("name", "") == "test_spec_id"):
            #     print(logger.get_logs())
            #     print(testcase.attributes)

    def testcase_execute(self, testcase,class_ins):
        # check the test case flag to execute or skip

        test_params = testcase.attributes.get("params", None)
        kwargs = {}
        params = {}
        if class_ins:
            # If it's a class method, pass the self instance
            params['self'] = class_ins

        if test_params is not None: 
            # Get the default parameters
            default_params = test_params.get("default", {})
            # Set the test step to one (initial)
            testcase.SetStep(1)

            for scenario_name, scenario_params in test_params.items():
                if scenario_name == "default":
                    continue  # Skip the default scenario, as it's already executed

                # Patch the default parameters with scenario-specific values
                scenario_params = {key: value for key, value in scenario_params.items() if key in default_params}
                patched_params = {**default_params.get("params", {}), **scenario_params.get("params", {})}

                # Add the scenario name to the kwargs
                kwargs['ts_name'] = scenario_name

                # Add the value parameters to the kwargs
                kwargs['ts_params'] = scenario_params.get("params", {})

                # Add the scenario reason to the kwargs
                kwargs['ts_detail'] = scenario_params.get("detail", {})

                params.update(patched_params) 

                self.execute_test(testcase,params,kwargs=kwargs)
                 
                # increment the test step
                testcase.IncStep()

        else:
            self.execute_test(testcase,params=params, kwargs=kwargs)

    def run_test(self):
        self.protester_collections.update_attribute("begin", self.protester_collections.get_time())
        for testsuite in self.protester_collections.testsuites:
            suite_class = testsuite.attributes.get("cls", None)
            
            # check for the dependency, execute only if true
            if self.dependency_check(testsuite, params= {}):
                # check the pre-execution conditions 
                pre_func = testsuite.attributes.get("pre", None)
                if callable(pre_func): pre_func()

                class_instance = None
                if suite_class is not None:
                    class_instance = suite_class()
                
                print("###################################################################")
                print(f"Running testsuite: {testsuite}")
                for testcase in testsuite.get_testcases():
                    print(f"Running testcase: {testcase}")
                    
                    testcase.update_attribute("begin", testcase.get_time())
                    self.testcase_execute(testcase, class_ins=class_instance)
                    testcase.update_attribute("end", testcase.get_time())
                    

                print("###################################################################")
                print("")

                # check the post-execution conditions 
                post_func = testsuite.attributes.get("post", None)
                if callable(post_func): post_func()

        self.protester_collections.update_attribute("end", self.protester_collections.get_time())

    def run_single_file(self, file):
        print(file)
        mod = self.load_module(file)
        self.load_tests(mod)

    def run(self):
        for test_file in self.test_files:
            self.run_single_file(test_file)
        
        # order the test suite sequence
        self.protester_collections.order_testsuites()
        
        # Add the ungrouped testcase to the main testcase collection
        if self.test_suite_ungrouped is not None:
            # Order the test cases by name/sequence
            self.test_suite_ungrouped.order_testcases()
            
            #adding test suit of ungrouped
            self.protester_collections.add_testsuite(self.test_suite_ungrouped)

        self.protester_collections.execute_protester_function("protester_pre_sut_setup", [],params={})
        self.run_test()
        self.protester_collections.execute_protester_function("protester_post_sut_setup", [],params={})

        total_test = self.successes + self.failures + self.not_x + self.skipped_x
        executed_test = self.successes + self.failures 

        test_info = {
            "begin": self.protester_collections.attributes.get("begin",
                        self.protester_collections.get_time()),
            "end":self.protester_collections.attributes.get("end",
                        self.protester_collections.get_time()),
        }

        statistics = [
            # total
            {
                "label": "Overall number of test cases",
                "count": total_test,
                "detail": ""
            },
            # executed
            {
                "label": "Executed test cases",
                "count": executed_test,
                "detail": f"{calculate_ratio(executed_test, total_test)}% of all test cases"
            },
            # not_executed
            {
                "label": "Not executed test cases",
                "count": self.not_x,
                "detail": f"{calculate_ratio(self.not_x, total_test)}% of all test cases"
            },
            # pass
            {
                "label": "Test cases passed",
                "count": self.successes,
                "detail": f"{calculate_ratio(self.successes, executed_test)}% of executed test cases"
            },
            # fail
            {
                "label": "Test cases failed",
                "count": self.failures,
                "detail": f"{calculate_ratio(self.failures, executed_test)}% of executed test cases"
            },
        ]
        overall_test_result = "Pass" if executed_test == (self.successes) else "Fail"

        
        if total_test > 0 :
            self.generate_report(overall_result = overall_test_result,
                            test_info=test_info, statistics=statistics)
        
        

        print("\n============")
        print(f"Total number of tests: {self.successes + self.failures}")
        if self.failures == 0:
            print(f"{colors.GREEN}tests succeeded{colors.RESET}")
        else:
            print(f"{colors.RED}{self.failures} tests failed{colors.RESET}")

def main():
    Runner(sys.argv[1]).run()
