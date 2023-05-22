import traceback

import openai

from base_modules.inqury import GPT_turbo
from base_modules.prompt import prompt_settings
from base_modules.code_management import meta_python
from base_modules.code_management import overtime_kill


class AutoFunction:

    def __init__(self, Objective, File_path, Minimum_trial, Resume, Input=None,
                 Output=None, Time_limit=60, Environment=None, Infinity_mode=False, Key=None, Verbose=False):

        self.Objective = Objective
        self.File_path = File_path
        self.Minimum_trial = Minimum_trial
        self.Resume = Resume
        self.Input = Input
        self.Output = Output
        self.Time_limit = Time_limit
        self.Environment = Environment
        self.Infinity_mode = Infinity_mode
        self.Key = Key
        self.Verbose = Verbose

        self.trial_count = 0
        self.debug_required = False
        self.result_length_sufficient = False
        self.execution_killed = False
        self.combined_raw_code, self.error, self.stdout, self.tb, self.response, \
        self.retrieved_code = "", "", "", "", "", ""

        if self.Output == None:
            self.No_output = True
        else:
            self.No_output = False

        self.meta_instance = meta_python(self.File_path, Output=self.Output, Verbose=self.Verbose)
        self.prompt = prompt_settings(self.Input, self.Output, self.Objective, self.Environment)
        self.prompt.input_and_output_type()

    def run(self):
        while True:
            try:
                print(f"---------Iteration {self.trial_count + 1} starts!---------")
                self.trial_count += 1
                self.debug_required = False

                if self.Resume:
                    self.read_run_and_test_previous_code()

                if self.Verbose:
                    print("Monitoring attributes:", self.debug_required, self.trial_count, self.Minimum_trial,
                          self.result_length_sufficient, self.execution_killed, len(self.stdout), self.Output,
                          self.No_output,
                          self.Infinity_mode)

                if self.debug_required == False and self.trial_count > self.Minimum_trial and self.result_length_sufficient == True and self.execution_killed == False and (
                        len(self.stdout) != 0 or self.Output == None or "save" in self.combined_raw_code
                        or self.No_output == True) and self.Infinity_mode == False:
                    print("AutoFunction reaches the termination criteria!")
                    break

                if not self.debug_required:
                    if (self.Resume == False and self.trial_count > 1) or self.Resume == True:
                        print("Begin improving the code")
                    else:
                        print("Begin creating the code")

                print("Thinking right now...")

                if self.trial_count == 1:
                    GPT_turbo_management = GPT_turbo(self.Key)
                    GPT_turbo_management.set_initial_time()
                else:
                    GPT_turbo_management.control_inquiry_frequency()

                self.send_inquiry()

                self.retrieve_code_and_test_length()

                if self.result_length_sufficient:
                    self.meta_instance.write(self.retrieved_code)
                    print(f"---------Iteration {self.trial_count} succeeded!---------")
            except Exception as fail:
                result = False
                print(f"---------Iteration {self.trial_count} failed!---------")
                print("Reason of failure:", str(traceback.format_exc()))

    def read_run_and_test_previous_code(self):
        self.meta_instance.read()
        self.meta_instance.compile()
        self.combined_raw_code = self.meta_instance.combined_raw_code

        if self.Output != None:
            output_required = True
        else:
            output_required = False

        # self.meta_instance.execute_and_test(output_required, True, 2000)

        self.execution_killed, shared_variables = overtime_kill(self.meta_instance.execute_and_test,
                                                                target_function_args=(output_required, True, 2000,),
                                                                time_limit=self.Time_limit)
        if not self.execution_killed:
            self.stdout = shared_variables["stdout"]
            self.error = shared_variables["error"]
            self.tb = shared_variables["tb"]
            self.debug_required = self.meta_instance.buggy

    def send_inquiry(self):
        self.prompt.reset()

        if self.Resume:

            if self.execution_killed:
                self.prompt.action_type("Killed", self.combined_raw_code, self.error, self.stdout, self.tb)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=self.prompt.prompt_message
                )
            else:
                if self.debug_required:
                    self.prompt.action_type("Debug", self.combined_raw_code, self.error, self.stdout, self.tb)
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=self.prompt.prompt_message
                    )
                else:
                    self.prompt.action_type("Improve", self.combined_raw_code, self.error, self.stdout, self.tb)
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=self.prompt.prompt_message
                    )
        else:
            self.prompt.action_type("Create", self.combined_raw_code, self.error, self.stdout, self.tb)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.prompt.prompt_message
            )

        response = response.choices[0].message.content
        self.response = response

        print("modification during this iteration:\n", self.response)

        if self.Verbose:
            print("type of the raw response:", type(self.response))
            print("raw response:", repr(self.response))

        self.Resume = True

    def retrieve_code_and_test_length(self):
        self.result_length_sufficient = True
        if self.trial_count == 1:
            self.retrieved_code = GPT_turbo.extract_code_from_GPT_turbo(self.response)
        else:
            if len(GPT_turbo.extract_code_from_GPT_turbo(self.response)) >= 0.5 * len(self.retrieved_code):
                self.retrieved_code = GPT_turbo.extract_code_from_GPT_turbo(self.response)
            else:
                print(f"---------Iteration {self.trial_count} failed!---------")
                print("Reason of failure: the modified code is too short, change aborted")
                self.result_length_sufficient = False
        if self.Verbose:
            print("the generated code is", self.retrieved_code)
