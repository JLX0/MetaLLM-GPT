import traceback
import time

import openai
from langchain.chat_models import ChatOpenAI

from base_modules.inqury import GPT_turbo
from base_modules.prompt import prompt_settings
from base_modules.code_management import meta_python
from base_modules.code_management import overtime_kill, execute
from base_modules.interface import CodeBlob


class MetaLLM_GPT:

    def __init__(self, Objective, File_path, Minimum_trial, Resume, Input=None,
                 Output=None, Time_limit=60, Privilege=False, Environment=None, Infinity_mode=False, Key=None, Model="3.5",
                 minimum_time_interval=5, Verbose=False):

        self.Objective = Objective
        self.File_path = File_path
        self.Minimum_trial = Minimum_trial
        self.Resume = Resume
        self.Input = Input
        self.Output = Output
        self.Time_limit = Time_limit
        self.Privilege = Privilege
        self.Environment = Environment
        self.Infinity_mode = Infinity_mode
        self.Key = Key
        self.Verbose = Verbose

        self.trial_count = 0
        self.prev_retrieved_code = ""
        self.previous_start = time.time()
        self.minimum_time_interval = minimum_time_interval

        if Model == "3.5":
            self.model = "gpt-3.5-turbo"
        elif Model == "4":
            self.model = "gpt-4"
        else:
            raise Exception("Model should be either 3.5 or 4")

        self.No_output = (self.Output is None)

        self.llm = ChatOpenAI(model=self.model, openai_api_key=self.Key, max_retries=1, max_tokens=None)
        self.meta_instance = meta_python(self.File_path, Output=self.Output, Verbose=self.Verbose)
        self.prompt = prompt_settings(self.Input, self.Output, self.Objective, self.Privilege, self.Environment)
        self.prompt.input_and_output_type()

    def run(self):
        self.result_length_sufficient = False
        while True:
            try:
                print(f"---------Iteration {self.trial_count + 1} starts!---------")
                self.trial_count += 1

                if self.Verbose:
                    print("Monitoring attributes:", self.trial_count, self.Minimum_trial,self.Output,
                          self.No_output,
                          self.Infinity_mode)

                if self.trial_count > 1:
                    self.control_inquiry_frequency()

                codeblob = None
                if self.Resume:
                    code = self.meta_instance.read()
                    codeblob = self.run_and_test_code(code)
                    if self.Verbose:
                        print(f"{codeblob=}")
                    if not codeblob.buggy and \
                        self.trial_count > self.Minimum_trial and \
                        self.result_length_sufficient and \
                        not codeblob.execution_killed and \
                        (len(codeblob.stdout) != 0 or \
                            self.Output is None or \
                            "save" in codeblob.code or \
                            self.No_output)\
                        and not self.Infinity_mode:
                        print("MetaLLM-GPT reaches the termination criteria!")
                        break
                    print("Begin improving the code")
                else:
                    print("Begin creating the code")

                print("Thinking right now...")
                prompt = self.prompt.generate_prompt(codeblob)
                response_txt = self.call_LLM(prompt)

                retrieved_code = self.retrieve_code_and_test_length(response_txt)

                if self.result_length_sufficient:
                    self.meta_instance.write(retrieved_code)
                    print(f"---------Iteration {self.trial_count} succeeded!---------")
            except Exception as fail:
                time.sleep(1)
                result = False
                print(f"---------Iteration {self.trial_count} failed!---------")
                print("Reason of failure:", str(traceback.format_exc()))

    def run_and_test_code(self, code: str) -> CodeBlob:
        output_required = (self.Output is not None)
        codeblob = overtime_kill(execute,
                                target_function_args=(
                                    code, 
                                    output_required, 
                                    True, 
                                    2000,
                                    self.Privilege,), 
                                time_limit=self.Time_limit)
        return codeblob

    def call_LLM(self, prompt):
        response = self.llm(prompt)
        response_txt = response.content
        # TODO: log token usage here
        print("modification during this iteration:\n", response_txt)

        if self.Verbose:
            print("type of the raw response:", type(response))
            print("raw response:", repr(response))

        self.Resume = True
        return response_txt

    def retrieve_code_and_test_length(self, response_txt):
        self.result_length_sufficient = True
        retrieved_code = None
        if self.trial_count == 1:
            retrieved_code = GPT_turbo.extract_code_from_GPT_turbo(response_txt)
        else:
            if len(GPT_turbo.extract_code_from_GPT_turbo(response_txt)) >= 0.5 * len(self.prev_retrieved_code):
                retrieved_code = GPT_turbo.extract_code_from_GPT_turbo(response_txt)
            else:
                print(f"---------Iteration {self.trial_count} failed!---------")
                print("Reason of failure: the modified code is too short, change aborted")
                self.result_length_sufficient = False
        if self.Verbose:
            print("the generated code is", retrieved_code)
        if retrieved_code is not None:
            self.prev_retrieved_code = retrieved_code
        return retrieved_code

    def set_initial_time(self):
        self.previous_start = time.time()

    def control_inquiry_frequency(self):
        current_start = time.time()
        time_left = self.minimum_time_interval - (current_start - self.previous_start)
        if time_left >= 0:
            print(f"Waiting for {time_left} seconds to avoid API overuse.")
            time.sleep(time_left + 0.1)

        self.previous_start = time.time()