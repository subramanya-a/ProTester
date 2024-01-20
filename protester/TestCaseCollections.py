from collections import OrderedDict
import random
from datetime import datetime
from inspect import isfunction, ismethod,isclass 


class StepLog:
    def __init__(self):
        self.logs_list = []

    def add_log(self, value):
        self.logs_list.append(value)

    def remove_log(self, index):
        if 0 <= index < len(self.logs_list):
            del self.logs_list[index]

    def get_logs(self):
        return list(self.logs_list)

    def clear_logs(self):
        self.logs_list.clear()


# class Tester:
#     def __init__(self, collection) -> None:
#         self.step = None
#         self.collection = collection

#     def SetStep(self,step:int):
#         self.step = step 

#     def IncStep(self):
#         if self.step is not None:
#             self.step += 1
#     def log_steps(self,step, result, status):
#         log = self.collection.attributes.get("steps", None)
#         if log is not None:
#             log.add_log({step, result, status})

#     def TestPass(self,result, step=""):
#         print(f"{self.step}:[PASS] {result}")
#         print(dir(self.collection))
        
#         if step is not None :
#             # string step in the report 
#             self.log_steps(step,
#                         result,
#                         self.collection.verbose("P"))  # Update the 'result' attribute in Collection
#         else:
#             # step number 
#             self.log_steps(self.step,
#                         result,
#                         self.collection.verbose("P"))  # Update the 'result' attribute in Collection        

#     def TestFail(self,result, step=""):
#         print(f"{self.step}:[FAIL] {result}")
#         if step is not None :
#             # string step in the report 
#             self.log_steps(step,
#                         result,
#                         self.collection.verbose("F"))  # Update the 'result' attribute in Collection
#         else:
#             # step number 
#             self.log_steps(self.step,
#                         result,
#                         self.collection.verbose("F"))  # Update the 'result' attribute in Collection  


class Info:
    class Group:
        def __init__(self,heading,table=None) -> None:
            if table is None:
                table = []
            self.group = {"heading": heading, "tables": table}
            
        def add_table_item(self, label, detail):
            self.group["tables"].append({"label": label, "detail": detail})

    def __init__(self):
        self.list = []
        
    def add_header(self, heading):
        header_instance = self.Group(heading,[])
        self.list.append(header_instance.group)
        return header_instance

    def get_instance_by_name(self, heading):
        for section in self.list:
            if section["heading"] == heading:
                return section
        return None
    
    def get_infos(self):
        return list(self.list)


class Collection:
    RESULTS = {"P": "Pass", "F":"Fail", "S":"Skipped", "SX":"Skipped Execution", "NX": "Not Executed", "LOG":"-"}
    def __init__(self):
        self.attributes = OrderedDict()
        self.attributes["result"] = {"status": self.RESULTS.get("NX"), "msg": ""}

    def add_attribute(self, key, value):
        self.attributes[key] = value

    def remove_attribute(self, key):
        self.attributes.pop(key, None)

    def update_attribute(self, key, value):
        # Check if the attribute exists
        if key in self.attributes:
            # Update the existing attribute
            self.attributes[key] = value
        else:
            # If the attribute doesn't exist, add it
            self.add_attribute(key, value)
        

    def get_attributes(self):
        return list(self.attributes.items())

    def clear_attributes(self):
        self.attributes.clear()

    def verbose(self, result_code):
        return self.RESULTS.get(result_code, result_code)

    def get_time(self):
        # 2023-12-31 15:19:36	(logging timestamp 6.510000)
        # Get the current timestamp
        current_timestamp = datetime.now()
        # Format the timestamp as per your requirement
        # formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S (logging timestamp %f)")

        # Extract the date and time components
        date_component = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        milliseconds_component = current_timestamp.strftime("%f")

        # Create a dictionary
        timestamp_dict = {
            'timestamp': date_component,
            'ms': milliseconds_component
        }
        # Print the result
        return timestamp_dict
    
    def set_attributes(self, name, func, doc=None) :

        # adding  preconditions
        self.attributes["doc"] = doc
        self.attributes["pre"] =  getattr(func, 'setup_function', None)
        self.attributes["post"] = getattr(func, 'teardown_function', None)
        self.attributes["params"] = getattr(func, '_test_params', None)
        # for each test parameters below items will repeat 
        self.attributes["name"] = name
        self.attributes["id"] = getattr(func, 'id', None)
        self.attributes["description"] = getattr(func, 'description', "No Description")
        self.attributes["extra"] = getattr(func, 'extra_tags', None)
        if isclass(func):
            self.attributes["cls"] = func
        else:
            self.attributes["func"] = func
        self.attributes["sequence"] = getattr(func, '_sequence_index', float('inf')) # testcase sequence should not none 
        self.attributes["variants"] = getattr(func, 'variants', [])
        self.attributes["skipif"] = getattr(func, 'skipif', [])
        self.attributes["executeif"] = getattr(func, 'executeif', [])
        self.attributes["result"] = {"status":self.verbose("NX"), "detail":"default detail"}
        self.attributes["steps"] = StepLog()

        
    def __getattr__(self, name):
        return self.attributes.get(name, None)
    
class TestCaseCollection(Collection):
    def __init__(self):
        super().__init__()
        
    def __repr__(self):
        return f"TestCase [{self.attributes.get('sequence', '')}]: {self.attributes.get('name', '')}"

    def SetStep(self,step:int):
        self.step = step 

    def IncStep(self):
        if self.step is not None:
            self.step += 1
    def log_steps(self,step, result, status):
        log = self.attributes.get("steps", None)
        timestamp = self.get_time()
        if log is not None:
            log.add_log({
                "timestamp": timestamp,
                "step":step,
                "result":result,
                "status":status})

    def TestLog(self,result, step=None):
        print(f"{self.step}:[LOG] {result}")
        
        if step is not None :
            # string step in the report 
            self.log_steps(step,
                        result,
                        self.verbose("LOG"))  # Update the 'result' attribute in Collection
        else:
            # step number 
            self.log_steps(self.step,
                        result,
                        self.verbose("LOG"))  # Update the 'result' attribute in Collection 
    
    def TestPass(self,result, step=None):
        print(f"{self.step}:[PASS] {result}")
        
        if step is not None :
            # string step in the report 
            self.log_steps(step,
                        result,
                        self.verbose("P"))  # Update the 'result' attribute in Collection
        else:
            # step number 
            self.log_steps(self.step,
                        result,
                        self.verbose("P"))  # Update the 'result' attribute in Collection  

    def TestFail(self,result, step=None):
        print(f"{self.step}:[FAIL] {result}")
        if step is not None :
            # string step in the report 
            self.log_steps(step,
                        result,
                        self.verbose("F"))  # Update the 'result' attribute in Collection
        else:
            # step number 
            self.log_steps(self.step,
                        result,
                        self.verbose("F"))  # Update the 'result' attribute in Collection  

class TestSuiteCollection(Collection):
    def __init__(self):
        super().__init__()
        self.testcases = []

    def add_testcase(self, testcase):
        self.testcases.append(testcase)

    def remove_testcase(self, index):
        if 0 <= index < len(self.testcases):
            del self.testcases[index]

    def get_testcases(self):
        return self.testcases

    def clear_testcases(self):
        self.testcases.clear()

    def order_testcases(self, key='sequence'):

        self.testcases = sorted(self.testcases, key=lambda x: x.attributes.get(key, float('inf')))
        
    def __repr__(self):
        return f"Test Suite Group: {self.attributes.get('name', '')}"

class ProTesterCollections(Collection):
    def __init__(self):
        super().__init__()
        self.testsuites = []
        self.pro_tester_modules = []

    def add_testsuite(self, testsuite):
        self.testsuites.append(testsuite)

    def remove_testsuite(self, index):
        if 0 <= index < len(self.testsuites):
            del self.testsuites[index]

    def get_testsuites(self):
        return self.testsuites

    def clear_testsuites(self):
        self.testsuites.clear()

    def order_testsuites(self, key='sequence'):
        self.testsuites = sorted(self.testsuites, key=lambda x: x.attributes.get(key, float('inf')))
    
    def execute_protester_function(self,function_name, result_default= None, params={}):
        """
        Execute the function with the specified name from the list of dictionaries.

        Parameters:
        - function_name (str): Name of the function to execute.
        - result_default : return if the function doesn't exist.

        Returns:
        - result: The result of executing the function. If the function doesn't exist, returns None.
        """
        # check if the variant parameter is empty, if empty return default result
        # if not params.get("variants"):
        #     return result_default
        
        matching_function_info = next((info for info in self.pro_tester_modules if info['name'] == function_name), None)

    
        if matching_function_info:
                
            return_value = matching_function_info['func'](**params)
            
            # if no response/None response from function, return default value 
            if return_value is not None:
                return return_value
                
        return result_default
    
    # def run_tests(self):
    #     for testsuite in self.testsuites:
    #         print("###################################################################")
    #         print(f"Running testsuite: {testsuite}")
    #         for testcase in testsuite.get_testcases():
    #             print(f"Running testcase: {testcase}")
    #             for pre_func in testcase.attributes.get("pre", []):
    #                 pre_func()

    #             testcase.attributes.get("func", lambda: None)()
                
    #             for post_func in testcase.attributes.get("post", []):
    #                 post_func()
    #         print("###################################################################")
    #         print("")



protester_collections = ProTesterCollections()




def test():
    TestCollections = ProTesterCollections()

    for suite in range(ord("a"), ord("c")):
        TestSuite = TestSuiteCollection()

        for i in range(1, 5):
            sequence = round(random.uniform(1.0, 5.0), 2)
            Testcase = TestCaseCollection()
            Testcase.add_attribute("pre", [lambda i=i: print(f"Running setup before testcase {i}")])
            Testcase.add_attribute("post", [lambda i=i: print(f"Running teardown after testcase {i}")])
            Testcase.add_attribute("sequence", f"{sequence}")
            Testcase.add_attribute("name", f"testcase {i}")
            Testcase.add_attribute("id", f"TC10{i}")
            Testcase.add_attribute("description", f"This is testcase {i}")
            Testcase.add_attribute("extra", [])
            Testcase.add_attribute("func", lambda i=i: print(f"Running func {i}"))
            Testcase.add_attribute("variant", ["variant A"])
            Testcase.add_attribute("skipif", bool((1 == 1) and (5 == 5)))
            Testcase.add_attribute("executeif", bool((1 == 1) and (5 == 5)))
            Testcase.add_attribute("result", Testcase.verbose("NX")) 

            TestSuite.add_testcase(Testcase)

        # Order the test cases by name
        TestSuite.order_testcases()
        
        
        TestSuite.add_attribute("pre", [lambda s=chr(suite): print(f"Running setup before testsuite {s}")])
        TestSuite.add_attribute("post", [lambda s=chr(suite): print(f"Running teardown after testsuite {s}")])
        TestSuite.add_attribute("sequence", "1.0.1")
        TestSuite.add_attribute("name", f"TestSuite {chr(suite)}")
        TestSuite.add_attribute("id", f"TC10{i}")
        TestSuite.add_attribute("description", f"This is testsuite {chr(suite)}")
        TestSuite.add_attribute("extra", [])
        TestSuite.add_attribute("funcs", TestSuite.get_testcases())
        TestSuite.add_attribute("variant", ["variant A"])
        TestSuite.add_attribute("skipif", bool((1 == 1) and (5 == 5)))
        TestSuite.add_attribute("executeif", bool((1 == 1) and (5 == 5)))
        TestSuite.add_attribute("result", TestSuite.verbose("NX")) 

        TestCollections.add_testsuite(TestSuite)

    TestCollections.run_tests()


# test()

# from decorators import info , sequence, exec_decorator, parameters, set_variable   


# @info(testcase="TC001", description="Test Case 1", extra_tags=["tag1", "tag2"])
# @sequence(1.0)
# @exec_decorator(setup_function=lambda: print("Setting up..."), teardown_function=lambda: print("Tearing down..."))
# # @parameters({
# #     "default": {"abc": "value", "xyz": "value"},
# #     "test_scenario1": {"abc": "patched_value"},
# #     "test_scenario2": {"xyz": "patched_value"},
# # })
# @parameters({
#     "default": {
#         "params": {"abc": "value", "xyz": "value"}, 
#         "detail": "Default scenario"},
#     "test_scenario1": {
#         "params": {"abc": "patched_value"},
#         "detail": "Scenario 1"},
#     "test_scenario2": {
#         "params": {"xyz": "patched_value"},
#         "detail": "Scenario 2"},
# })
# def test_info(protest:Tester, abc, xyz, **kwargs):
#     print(f"Running test for scenario: {TS_NAME}")
#     print(f"parameters: abc: {abc} xyz: {xyz}")
#     print(kwargs.get('ts_name', None))
#     print("Test function body")
#     # protest.SetStep(1)
#     protest.TestPass(">>>>>>>>>>>data passed")

    
# # Accessing attributes in the runner
# function_id = getattr(test_info, 'testcase', None)
# function_description = getattr(test_info, 'description', None)
# function_extra_tags = getattr(test_info, 'extra_tags', None)
# function_sequence_index  = getattr(test_info, '_sequence_index', None)

# # Accessing attributes
# setup_attribute = getattr(test_info, 'setup_function', None)
# teardown_attribute = getattr(test_info, 'teardown_function', None)

# print(f"Setup attribute: {setup_attribute}")
# print(f"Teardown attribute: {teardown_attribute}")
# print(function_sequence_index)

# print(f"ID: {function_id}, Description: {function_description}, Extra Tags: {function_extra_tags}")

# test_info(protest=Tester())

# sut_configs = Info()
# sut_configs_inst = sut_configs.add_header("Test Engineer")
# sut_configs_inst.add_table_item("Windows Login Name: ", "username")

# print(sut_configs.get_infos())
# # for item in sut_configs.get_infos():
# #     print(item.group)
