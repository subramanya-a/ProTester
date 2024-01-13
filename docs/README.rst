ProTester Documentation
=======================

Introduction
------------
ProTester is a Python test automation framework designed to provide a straightforward interface for automating tests with built-in functionalities. The library offers convenient decorators for defining test case order, capturing requirements, managing session functions, handling dependencies, and more.

Features
--------
1. **Testcase Order of Execution:** The `@sequence(index)` decorator orders test cases during execution based on the provided index.

2. **Testcase Requirement Capture:** The `@info(id, description, extra_tags)` decorator captures essential information in the report file.

3. **Testcase Execution Session Functions:** The `@session_exec(setup_function, teardown_function)` decorator calls setup and teardown functions on each execution.

4. **Testcase Execution Dependency Checks:** The `@dependency(variants, skipif, executeif)` decorator performs dependency checks before execution. If any condition is set, the execution is skipped for the next testcase.

5. **Parameter Testing (Under Development):** Feature for testing parameters.

6. **Multiple Iteration Testing (Under Development):** Feature for testing multiple iterations.

7. **Parallel Execution (Under Development):** Feature for executing test cases in parallel.

Installation
------------
To install ProTester, use the following command:

```
$ python setup.py install
```
or

```
$ pip install git+https://github.com/subramanya-a/ProTester.git
```

## Project Contributors

- [Subramanya A](https://github.com/subramanya-a/) (@Subramanya.a)

---
[MIT License](https://github.com/subramanya-a/ProTester/blob/master/docs/LICENSE) | Built with the [ProTester](https://pypi.python.org/pypi/ProTester)
