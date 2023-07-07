import sys, os
from base_modules.interface import CodeBlob
from base_modules.code_management import overtime_kill, execute

# sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))


def test_example():
    assert(1+2==3)

def assert_codeblob_type(codeblob: CodeBlob):
    """

    class CodeBlob(NamedTuple):
        code: str = ""
        stdout: Optional[str] = ""
        error: Optional[str] = ""
        tb: Optional[str] = ""
        buggy: Optional[bool] = False
        execution_killed: bool = False
        execution_time: float = 0.0
        environment: Optional[Any] = None # Not sure about this one
    """
    # assert that the type of all field is valid
    assert(type(codeblob.code) == str)
    assert(type(codeblob.stdout) == str)
    assert(type(codeblob.error) == str)
    assert(type(codeblob.tb) == str)
    assert(type(codeblob.buggy) == bool or codeblob.buggy == None)
    assert(type(codeblob.execution_killed) == bool)
    assert(type(codeblob.execution_time) == float, codeblob.execution_time>=0.0)
    # assert(type(codeblob.environment) == type(None))
    

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