from base_modules.interface import CodeBlob
from base_modules.code_management import overtime_kill, execute


def assert_codeblob_type(codeblob: CodeBlob):
    """
        assert that the type of all fields of codeblob is valid
    """
    assert(type(codeblob.code) == str)
    assert(type(codeblob.stdout) == str)
    assert(type(codeblob.error) == str)
    assert(type(codeblob.tb) == str)
    assert(type(codeblob.buggy) == bool or codeblob.buggy == None)
    assert(type(codeblob.execution_killed) == bool)
    assert(type(codeblob.execution_time) == float, codeblob.execution_time>=0.0)
    # assert(type(codeblob.environment) == type(None))


working_import_code = """
import random
def random_int():
    return random.randint(0, 100)
print(random_int())
"""
def test_working_import_code():
    output_required = True
    privilege = True
    codeblob = overtime_kill(execute,
                            target_function_args=(
                                working_import_code, 
                                output_required, 
                                True, 
                                2000,
                                privilege,), 
                            time_limit=5)
    assert_codeblob_type(codeblob)
    assert(int(codeblob.stdout) >= 0 and int(codeblob.stdout) <= 100)

buggy_code = """
import time
time.sleep(0.5)
assert(1==2)
"""
def test_execution_error_handling():
    output_required = True
    privilege = True
    codeblob = overtime_kill(execute,
                            target_function_args=(
                                buggy_code, 
                                output_required, 
                                True, 
                                2000,
                                privilege,), 
                            time_limit=5)
    assert_codeblob_type(codeblob)
    assert(codeblob.buggy == True)
    assert(codeblob.execution_killed == False)


infinite_loop_code = """
import time
while True:
    time.sleep(2)
"""
def test_infinite_loop_handling():
    output_required = True
    privilege = True
    codeblob = overtime_kill(execute,
                            target_function_args=(
                                infinite_loop_code, 
                                output_required, 
                                True, 
                                2000,
                                privilege,), 
                            time_limit=3)
    assert_codeblob_type(codeblob)
    assert(codeblob.buggy == False)
    assert(codeblob.execution_killed == True)
