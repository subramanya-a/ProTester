from protester.decorators import info , sequence, session_exec, parameters, dependency
from protester.conditions import is_pass, is_fail
from protester.TestCaseCollections import Info
import sys, os
from pathlib import Path
from specs.listener import setup_log_event_handlers, variant_event
from protester.event import post_event

############################################################################
#                       PRO TESTER CONFIG
############################################################################
def protester_sut_info(items:Info):
    """
    This method is called before or after all test to get the test module info
    """

    test_module = items.add_header("Violations occurred (not within test cases)")
    test_module.add_table_item("warning ", "some info to capture in the log")

    return items.get_infos()
    

def protester_pre_sut_setup():
    """
    This method is called before all test to setup the test env
    """
    # subscribe all log events
    setup_log_event_handlers()
    
    # Set test Variants
    post_event("test_variants", ["lite"])
    post_event("protester_log", "protester_pre_sut_setup completed" )
    
def protester_post_sut_setup():
    """
    This method is called after all test for re-test env
    """
    post_event("protester_log", "protester_post_sut_setup completed" )
    
def protester_is_variant_supported(variants: list) -> bool:
    """
    This method is called before all test to setup the test env
    """
    
    for variant in variants:
        if variant in variant_event.get_variants():
            return True, "Variant Lite B is supported"
    

    return False, "Skipping due to unsupported variant"

def protester_report_title():
    """
    return the report title
    """
    return "Tester"

def protester_sut_config(items:Info):
    """
    return the configuration data 
    time format 
    reporter client info
    plugin used
    etc.
    """
    test_setup = items.add_header("Test Setup")
    test_setup.add_table_item("Test Module Name 1: ", "TestSuite")
    test_setup.add_table_item("Test Module Name 2: ", "TestModule")

    test_env = items.add_header("Test Environment")
    test_env.add_table_item("Python Version: ", f"{sys.version}")
    test_env.add_table_item("Python Version Info: ", f"{sys.version_info}")
    test_env.add_table_item("Test Case Path: ", f"{Path().absolute()}")

    return items.get_infos()
    

############################################################################
#                       TESTCASE
############################################################################

def test_success(protest, *args, **kwargs):
    assert 1==1

def test_not_equal_success(protest, *args, **kwargs):
    assert 1!=1, "Not equal failure"

def test_failure(protest, *args, **kwargs):
    assert 0/2, "operation failed"

def test_not_equal_failure(protest, *args, **kwargs):
    assert (1*5)==1, "check failed 5 != 1"

class TEST_SUTE:
    """
    This Test Suite is sample tests which contains both positive and negative testcases 
    """
    @sequence(1.0)
    def test_suite_success(self, protest,**kwargs):
        assert 1==1
        
    @session_exec(setup_function=lambda: print("Setting up..."), teardown_function=lambda: print("Tearing down..."))
    def test_suite_failure(self, protest,**kwargs):
        assert 1!=1

@sequence(1.0)
@dependency(
    variants=["base", "lite"],
    skipif=[
        lambda: (1 != 1, "execution skip due to"),  # Example executeif condition 1
        # lambda: is_pass(""), # if none, will return false 
        # lambda: is_pass("TESTSUTE::test_suite_failure"),
        # lambda: is_pass("test_suite_success"),
        # lambda: is_pass("test_success"),
        # lambda: is_pass("test_not_equal_failure"),
        # lambda: is_fail("TESTSUTE::test_suite_failure"),
    ],
    executeif=[
        lambda: (1 != 1, "execution skip for 1==1 ")  # Example executeif condition 1
    ]
)
@session_exec(setup_function=lambda: print("test suite Setting up..."), teardown_function=lambda: print("test suite Tearing down..."))
class TEST_SEQ:
    """
    This Test Suite is sample tests which contains both positive and negative testcases 
    """
    @sequence(1.0)
    @info(id="TC051", description="Test Case description", extra_tags=["tag1", "tag2"])
    def test_2suite_success(self, protest,**kwargs):
        assert 1==1
    
    @info(id="TC051", description="Test Case description", extra_tags=["tag1", "tag2"])
    def test_2suite_failure(self, protest,**kwargs):
        assert 1!=1


def somefunc(some)-> (bool,str):
    return (False, "some reason to be skif, this condition is not skipped if false")


@info(id="TC001", description="Test Case 1", extra_tags=["tag1", "tag2"])
@sequence(1.0)
@dependency(
    variants=["base", "lite"],
    skipif=[
        lambda: (1 == 1, "execution skip due to"),  # Example executeif condition 1
        somefunc(""),
        # lambda: is_pass(""), # if none, will return false 
        # lambda: is_pass("TESTSUTE::test_suite_failure"),
        # lambda: is_pass("test_suite_success"),
        # lambda: is_pass("test_success"),
        # lambda: is_pass("test_not_equal_failure"),
        # lambda: is_fail("TESTSUTE::test_suite_failure"),
    ],
    executeif=[
        lambda: (1 != 1, "execution skip for 1==1 ")  # Example executeif condition 1
    ]
)
@session_exec(setup_function=lambda: print("Setting up..."), teardown_function=lambda: print("Tearing down..."))
def test_spec_id2(protest, *args, **kwargs):
    """
    sample test case descriptions or information 
    """
    assert 1==1
    protest.TestLog("Test function body")
    # protest.SetStep(1)
    protest.TestPass("data passed")



# @info(id="TC001", description="Test Case 1", extra_tags=["tag1", "tag2"])
# @sequence(1.0)
# @session_exec(setup_function=lambda: print("Setting up..."), teardown_function=lambda: print("Tearing down..."))
# @dependency(
#     variants=["base", "lite"],
#     skipif=[
#         lambda abc, xyz:( abc == xyz, f"value {abc} and {xyz} are equal, hence test is skipped"),  # Example skipif condition 1
#         lambda abc, xyz:( abc > xyz, ""),# Example skipif condition 2 (no message)
#         somefunc(""),
#     ],
#     executeif=[
#         lambda x, y: x != y    # Example executeif condition 1
#     ]
# )
# @parameters({
#     "default": {
#         "params": {"abc": 5, "xyz": 4}, 
#         "detail": "Default scenario"},
#     "test_scenario1": {
#         "params": {"abc": 2},
#         "detail": "Scenario 1"},
#     # "test_scenario2": {
#     #     "params": {"xyz": 1},
#     #     "detail": "Scenario 2"},
# })
# def test_spec_id(protest, abc, xyz, *args, **kwargs):
#     assert 1==1
#     protest.TestLog(f"{kwargs.get('ts_name', None)}")
#     protest.TestLog(f"Running test for scenario: {kwargs.get('ts_name', None)}")
#     protest.TestLog(f"parameters: abc: {abc} xyz: {xyz}")
#     protest.TestLog("Test function body")
#     # protest.SetStep(1)
#     protest.TestPass(">>>>>>>>>>>data passed")

