import io
from contextlib import redirect_stdout
import traceback
import multiprocessing

class meta_python():

    def __init__(self, File_path, Output=None, Verbose=False):
        self.File_path = File_path
        self.Verbose = Verbose
        self.Output = Output

        self.combined_code = ""
        self.codeObject = ""
        self.stdout = ""
        self.past_error_history = []
        self.buggy = False
        self.error = ""
        self.stdout = ""
        self.tb = ""

    def read(self):
        file = open(self.File_path, "r")
        line_list = file.readlines()
        if self.Verbose:
            print("raw string line by line:")
            for line in line_list:
                print(repr(line))
        self.combined_code = "".join(str(item) for item in line_list)
        if self.Verbose:
            print("raw string combined:")
            print("combined_list", repr(self.combined_code))

    def write(self,the_code):
        f = open(self.File_path, "w")
        f.write(the_code)
        f.close()

    def compile(self):
        try:
            self.codeObject = compile(self.combined_code, 'sumstring_1', 'exec')
        except:
            print("The compilation process failed")

    def execute_and_test_base(self, output_required=False, capture_error=False):

        print("Begin running the code")

        try:
            f = io.StringIO()
            with redirect_stdout(f):
                exec(self.codeObject, globals())
            self.stdout = f.getvalue()
            print("The code runs smoothly")
            if (output_required or self.Output != None) and "save" not in self.combined_code:
                if len(self.stdout) == 0:
                    print("However, the code lacks a function call or valid output")
                else:
                    print("Output of the code:\n" + self.stdout)

        except Exception as e:
            if capture_error:
                self.error = str(e)
                self.past_error_history.append(self.error)
                self.tb = str(traceback.format_exc())

            if e.__class__.__name__ == 'ModuleNotFoundError':
                print("The generated code cannot be tested due to missing packages. It is advised to either change "
                      "the objective, describe your current environment, or install the missing packages before "
                      "proceeding with AutoFunction")
                if capture_error:
                    print("The error message is:", self.error)
            else:
                print("The code is buggy")
                if capture_error:
                    print(self.tb)

            self.buggy = True

    def execute_and_test(self, output_required=False, capture_error=False):
        global_before = (globals().keys())
        if self.Verbose:
            print("global variables before testing:", global_before)

        self.execute_and_test_base(output_required, capture_error)

        global_after = (globals().keys())
        if self.Verbose:
            print("global variables after testing:", global_after)

        excessive_global = [x for x in global_after if x not in global_before]
        if self.Verbose:
            print("excessive global variables:", excessive_global)

        for n in excessive_global:
            del globals()[n]


def overtime_kill(target_function,target_function_args=None, time_limit=60):
    if target_function_args!=None:
        p = multiprocessing.Process(target=target_function, args=target_function_args)
    else:
        p = multiprocessing.Process(target=target_function)

    p.start()
    p.join(time_limit)

    if p.is_alive():
        print(f"The execution of the code takes longer than {time_limit} seconds, terminating the execution...")

        p.terminate()
        p.join()

        return True
    else:
        print("The execution of the code finishes in time")

        return False
