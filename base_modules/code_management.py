import io
from contextlib import redirect_stdout
import traceback
import multiprocessing


class meta_python():

    def __init__(self, File_path, Output=None, Verbose=False):
        self.File_path = File_path
        self.Verbose = Verbose
        self.Output = Output

        self.combined_raw_code = ""
        self.compiled_code = ""
        self.stdout = ""
        self.past_error_history = []  # check whether error repeats a lot?
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
        self.combined_raw_code = "".join(str(item) for item in line_list)
        if self.Verbose:
            print("raw string combined:")
            print("combined raw code", repr(self.combined_raw_code))

    def write(self, the_code):
        f = open(self.File_path, "w")
        f.write(the_code)
        f.close()

    def compile(self):
        try:
            self.compiled_code = compile(self.combined_raw_code, 'code_to_be_compiled', 'exec')
        except:
            print("The compilation process failed")

    def execute_and_test_base(self, output_required=False, capture_error=False, output_length_limit=None,
                              ignore_warning=False):

        print("Begin running the code")

        try:
            f = io.StringIO()
            with redirect_stdout(f):
                exec(self.compiled_code, globals())
            self.stdout = f.getvalue()
            print("The code runs smoothly")

            if output_length_limit is not None:
                if len(self.stdout) > output_length_limit:
                    print(f"Warning: The length of the standard output is too long, \
                                       MetaLLM-GPT only considers the last {output_length_limit} strings of the "
                          f"standard output.")
                    self.stdout = self.stdout[-output_length_limit:]

            if (output_required or self.Output is not None) and ("save" or "show") not in self.combined_raw_code:
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
                if not ignore_warning:
                    print("The generated code cannot be tested due to missing packages. It is advised to either change "
                          "the objective, describe your current environment, or install the missing packages before "
                          "proceeding with MetaLLM-GPT")
                if capture_error:
                    print("The error message is:", self.error)
            else:
                print("The code is buggy")
                if capture_error:
                    print(self.tb)

            self.buggy = True

    def execute_and_test(self, ret_dict, output_required=False, capture_error=False, output_length_limit=None,
                         ignore_warning=False):

        global_before = list(globals().keys())
        if self.Verbose:
            print("global variables before testing:", global_before)

        self.execute_and_test_base(output_required, capture_error, output_length_limit, ignore_warning=ignore_warning)

        global_after = list(globals().keys())
        if self.Verbose:
            print("global variables after testing:", global_after)

        excessive_global = [x for x in global_after if x not in global_before]
        if self.Verbose:
            print("excessive global variables:", excessive_global)

        for n in excessive_global:
            del globals()[n]

        ret_dict["stdout"], ret_dict["error"], ret_dict["tb"], ret_dict[
            "buggy"] = self.stdout, self.error, self.tb, self.buggy


def overtime_kill(target_function, target_function_args=None, time_limit=60, ret=True):
    # converting this function into a decorator might make it less convenient

    ret_dict = multiprocessing.Manager().dict()

    if target_function_args is not None:
        p = multiprocessing.Process(target=target_function, args=(ret_dict,) + target_function_args)
    elif ret:
        p = multiprocessing.Process(target=target_function, args=(ret_dict,))
    else:
        p = multiprocessing.Process(target=target_function)

    p.start()
    p.join(time_limit)
    if p.is_alive():
        print(f"The execution of the code takes longer than {time_limit} seconds, terminating the execution...")
        p.terminate()
        p.join()
        return True, dict(ret_dict)
    else:
        print("The execution of the code finishes in time")
        return False, dict(ret_dict)
