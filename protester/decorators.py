from functools import wraps, partial
from protester.TestCaseCollections import protester_collections

def before_test(func):
    func._run_before_test = True
    return func

def after_test(func):
    func._run_after_test = True
    return func


# class Preconditions:
#     def __init__(self):
#         self.setup_function = None
#         self.teardown_function = None
#         self._run_before_test = False
#         self._run_after_test = False

#     def before(self, setup_function):
#         self.setup_function = setup_function
#         self._run_before_test = True
#         return self

#     def after(self, teardown_function):
#         self.teardown_function = teardown_function
#         self._run_after_test = True
#         return self

#     def __call__(self, func):
#         def wrapper(*args, **kwargs):
#             if self.setup_function:
#                 self.setup_function()
            
#             result = func(*args, **kwargs)

#             if self.teardown_function:
#                 self.teardown_function()
            
#             return result

#         # Set _run_before_test and _run_after_test attributes if explicitly used
#         wrapper._run_before_test = self._run_before_test
#         wrapper._run_after_test = self._run_after_test
#         return wrapper



# class Preconditions:
#     def __init__(self):
#         self.setup_before = None
#         self.teardown_after = None

#     def before(self, setup_function):
#         self.setup_before = setup_function
#         return self

#     def after(self, teardown_function):
#         self.teardown_after = teardown_function
#         return self

#     def __call__(self, test_function):
#         def wrapper():
#             if self.setup_before:
#                 self.setup_before()

#             try:
#                 test_function()
#             finally:
#                 if self.teardown_after:
#                     self.teardown_after()

#         wrapper._preconditions = self  # Attach the Preconditions instance to the wrapper
#         return wrapper

def session_exec(setup_function=None, teardown_function=None):
    def decorator(test_function):
        @wraps(test_function)
        def wrapper(*args, **kwargs):
            # if wrapper.setup_function:
            #     print(f"Running setup before test in {test_function.__name__}")
            #     wrapper.setup_function()

            # try:
            #     print(f"Running main function: {test_function.__name__}")
            #     result = test_function(*args, **kwargs)
            # finally:
            #     if wrapper.teardown_function:
            #         print(f"Running teardown after test in {test_function.__name__}")
            #         wrapper.teardown_function()

            # return result
            return test_function(*args, **kwargs)

        wrapper.setup_function = setup_function
        wrapper.teardown_function = teardown_function

        return wrapper

    return decorator

def info(id, description="", extra_tags=[]):
    def decorator(func):
        setattr(func, 'id', id)
        setattr(func, 'description', description)
        setattr(func, 'extra_tags', extra_tags)
        
        # Check for required attributes
        required_attributes = ['id']
        for attribute in required_attributes:
            if not hasattr(func, attribute):
                raise AttributeError(f"{attribute} is required for the {func.__name__} function.")

        return func
    
    return decorator

# def info(testcase, description="", extra_tags=[]):
#     def decorator(func):
#         # print(f"Setting attributes for {func.__name__}: {testcase}, {description}, {extra_tags}")
#         func.testcase = testcase
#         func.description = description
#         func.extra_tags = extra_tags

#         # Check for required attributes
#         required_attributes = ['testcase']
#         for attribute in required_attributes:
#             if not hasattr(func, attribute):
#                 raise AttributeError(f"{attribute} is required for the {func.__name__} function.")
#         # function_id = getattr(func, 'testcase', None)
#         # function_description = getattr(func, 'description', None)
#         # function_extra_tags = getattr(func, 'extra_tags', None)

#         # print(f"ID: {function_id}, Description: {function_description}, Extra Tags: {function_extra_tags}")
#         # Check the attributes
#         # print("Attributes Set:", func.testcase, func.description, func.extra_tags)

#         return func

#     return decorator


def sequence(index):
    def decorator(func):
        func._sequence_index = index
        return func
    
    return decorator



from unittest.mock import patch
def set_variable(variable_name, value):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with patch.dict('__main__.__dict__', {variable_name: value}):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# def parameters(test_scenarios):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             # Get the default parameters
#             default_params = test_scenarios.get("default", {})

#             # Execute the default scenario first
#             # result_default = func(*args, parameters=default_params, **kwargs)
            
#             # You can do something with the result_default if needed

#             for scenario_name, scenario_params in test_scenarios.items():
#                 if scenario_name == "default":
#                     continue  # Skip the default scenario, as it's already executed

#                 # Patch the default parameters with scenario-specific values
#                 scenario_params = {key: value for key, value in scenario_params.items() if key in default_params}
#                 patched_params = {**default_params, **scenario_params}

#                 # Pass the patched parameters and scenario name to the function
#                 # result = func(*args, parameters=patched_params,**kwargs)
                    
#                 with patch.dict('__main__.__dict__', {"TS_NAME": scenario_name}):
#                     result = func(*args, parameters=patched_params,**kwargs)
#                 # You can do something with the result if needed

#             return result

#         return wrapper

#     return decorator

def parameters(test_params):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(kwargs)
            # protest = kwargs.get('protest', None)

            # # Get the default parameters
            # default_params = test_params.get("default", {})

            # # Execute the default scenario first
            # # result = func(*args, parameters=default_params, **kwargs)
            
            # # You can do something with the result_default if needed
            # if protest is not None:
            #     # Set the test step to one (initial)
            #     protest.SetStep(1)

            #     for scenario_name, scenario_params in test_params.items():
            #         if scenario_name == "default":
            #             continue  # Skip the default scenario, as it's already executed

            #         # Patch the default parameters with scenario-specific values
            #         scenario_params = {key: value for key, value in scenario_params.items() if key in default_params}
            #         patched_params = {**default_params.get("params", {}), **scenario_params.get("params", {})}


            #         # Add the scenario name to the kwargs
            #         kwargs['ts_name'] = scenario_name

            #         # Add the value parameters to the kwargs
            #         kwargs['ts_params'] = scenario_params.get("params", {})

            #         # Add the scenario reason to the kwargs
            #         kwargs['ts_detail'] = scenario_params.get("detail", {})

            #         result = func(*args, **patched_params, **kwargs)

            #         # Pass the patched parameters and scenario name to the function
            #         # with patch.dict('__main__.__dict__', {"TS_NAME": scenario_name}):
            #         #     # result = func(*args, parameters=patched_params, **kwargs)
            #         #     result = func(*args, **patched_params, **kwargs)
                        
            #         # increment the test step
            #         protest.IncStep()

            # You can do something with the result if needed
            pass
        
            # return result
            return func(*args, **kwargs)


        wrapper._test_params = test_params
        return wrapper

    return decorator

def dependency(variants=None, skipif=None, executeif=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # params={}
            # params["variants"]= variants
            # # Step 1: Check if variant is supported
            # if not protester_collections.execute_protester_function("protester_is_variant_supported",True, params):
            #     print(f"Skipping {test_function.__name__} due to unsupported variant")
            #     return

            # # Step 2: Check skip conditions
            # for condition in skipif:
            #     try:
            #         condition(*args, **kwargs)
            #     except Exception as e:
            #         print(e)
            # if skipif and any(condition(*args, **kwargs) for condition in skipif):
            #     print(f"Skipping {test_function.__name__} due to skip conditions")
            #     return

            # # Step 3: Check execute conditions
            # if executeif and not all(condition(*args, **kwargs) for condition in executeif):
            #     print(f"Skipping {test_function.__name__} due to execute conditions")
            #     return

            # Execute the actual test function
            # return result
            return func(*args, **kwargs)
        
        wrapper.variants = variants
        wrapper.skipif = skipif
        wrapper.executeif = executeif
        return wrapper

    return decorator