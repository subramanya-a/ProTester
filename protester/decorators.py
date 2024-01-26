from functools import wraps, partial
from protester.TestCaseCollections import protester_collections

def before_test(func):
    setattr(func, '_run_before_test', True)
    return func

def after_test(func):
    setattr(func, '_run_after_test', True)
    return func


def session_exec(setup_function=None, teardown_function=None):
    def decorator(func):
        setattr(func, 'setup_function', setup_function)
        setattr(func, 'teardown_function', teardown_function)
        return func

    return decorator

def info(id, description="", extra_tags=[]):
    def decorator(func):
        # Check if the object is a function
        if callable(func):
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

def sequence(index):
    def decorator(func):
        setattr(func, '_sequence_index', index)
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
        setattr(func, 'variants', variants)
        setattr(func, 'skipif', skipif)
        setattr(func, 'executeif', executeif)
        return func
    
    return decorator