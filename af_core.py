import openai
import traceback

from base_modules.inqury import GPT_turbo
from base_modules.prompt import prompt_settings
from base_modules.code_management import meta_python
from base_modules.code_management import overtime_kill


class AutoFunction:

    def __init__(self,Objective,File_path,Minimum_trial,Resume,Input=None,
                Output=None, time_limit=10, Environment=None, Infinity_mode=False, key=None,Verbose=False):

        self.Objective=Objective
        self.File_path=File_path
        self.Minimum_trial=Minimum_trial
        self.Resume=Resume
        self.Input=Input
        self.Output=Output
        self.time_limit=time_limit
        self.Environment=Environment
        self.Infinity_mode=Infinity_mode
        self.key=key
        self.Verbose=Verbose

        self.trial_count=0
        self.DEBUG=False
        self.result=False
        self.killed=False
        self.combined_code, self.error, self.stdout, self.tb, self.response,\
        self.the_code= "", "", "", "", "", ""
        if self.Output==None:
            self.No_output=True
        else:
            self.No_output=False

        self.meta_instance = meta_python(self.File_path, Output=self.Output, Verbose=self.Verbose)

    def run(self):
        while True:
            try:
                print(f"---------Iteration {self.trial_count + 1} starts!---------")
                self.trial_count += 1
                DEBUG = False

                if self.Resume:
                    self.read_run_and_test_previous_code()


                if DEBUG == False:
                    if (self.Resume == False and self.trial_count > 1) or self.Resume == True:
                        print("Begin improving the code")
                    else:
                        print("Begin creating the code")

                print("Thinking right now...")

                if self.trial_count==1:
                    GPT_turbo_management=GPT_turbo(self.key)
                    GPT_turbo_management.set_initial_time()
                else:
                    GPT_turbo_management.control_inquiry_frequency()

                if DEBUG == False and self.trial_count > self.Minimum_trial and self.result == True and self.killed== False and (
                        len(self.stdout) != 0 or self.Output == None or "save" in self.combined_code
                        or self.No_output == True) and self.Infinity_mode == False:
                    break

                self.send_inquiry()

                self.retrive_code_and_test()

                self.meta_instance.write(self.the_code)



                print(f"---------Iteration {self.trial_count} succeeded!---------")
            except Exception as fail:
                result = False
                print(f"---------Iteration {self.trial_count} failed!---------")
                print("Reason of failure:", str(traceback.format_exc()))

    def read_run_and_test_previous_code(self):
        self.meta_instance.read()
        self.meta_instance.compile()

        if self.Output != None:
            output_required = True
        else:
            output_required = False

        self.killed=overtime_kill(self.meta_instance.execute_and_test,target_function_args=(output_required,True), time_limit=self.time_limit)

        if self.killed==False:
            self.combined_code = self.meta_instance.combined_code
            self.stdout = self.meta_instance.stdout
            self.error = self.meta_instance.error
            self.tb = self.meta_instance.tb
            self.DEBUG = self.meta_instance.buggy



    def send_inquiry(self):
        prompt = prompt_settings(self.Input, self.Output, self.Objective, self.Environment)
        prompt.input_and_output_type()
        if self.Resume:

            if self.killed==True:
                prompt.action_type("Killed",self.combined_code,self.error,self.stdout,self.tb)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=prompt.prompt_message
                )
            else:
                if self.DEBUG:
                    prompt.action_type("Debug",self.combined_code,self.error,self.stdout,self.tb)
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=prompt.prompt_message
                    )
                else:
                    prompt.action_type("Improve",self.combined_code,self.error,self.stdout,self.tb)
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=prompt.prompt_message
                    )
        else:
            prompt.action_type("Create",self.combined_code,self.error,self.stdout,self.tb)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt.prompt_message
            )


        response = response.choices[0].message.content
        self.response= response

        print("modification during this iteration:\n", self.response)

        if self.Verbose:
            print("type of the raw response:", type(self.response))
            print("raw response:", repr(self.response))

        self.Resume = True
        self.result = True

    def retrive_code_and_test(self):
        if self.trial_count == 1:
            self.the_code = GPT_turbo.find_string_in_the_middle(self.response)
        else:
            if len(GPT_turbo.find_string_in_the_middle(self.response)) >= 0.5 * len(self.the_code):
                self.the_code = GPT_turbo.find_string_in_the_middle(self.response)
            else:
                print(f"---------Iteration {self.trial_count} failed!---------")
                print("Reason of failure: the modified code is too short, change aborted")
                result = False
        if self.Verbose:
            print("the generated code is", self.the_code)