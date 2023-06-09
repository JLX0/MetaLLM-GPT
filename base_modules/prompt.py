from copy import deepcopy


class prompt_settings:
    base_prompt_message = [{"role": "system", "content": "You are a programming expert."},
                           {"role": "system",
                            "content": "The code should always include at least one function call inside it to "
                                       "demonstrate an execution"},
                           {"role": "system", "content": "For your response, you should strictly follow the format "
                                                         "```python <python code that includes at least one function "
                                                         "call to demonstrate an execution> ```  <Explanation about "
                                                         "the generated code>"},
                           {"role": "system",
                            "content": "You should always write all of the codes you generated in a single block. Any "
                                       "python codes in your response should always start with ```python and end with"
                                       " ```."},
                           {"role": "system",
                            "content": "You should always include the full code in your response, instead of simply "
                                       "the modified part of the code or the function call."},
                           {"role": "system",
                            "content": "You are forbidden to only include the modified part of the code in your "
                                       "response."},
                           {"role": "system",
                            "content": "You are forbidden to only include the function call of the code in your "
                                       "response."},
                           {"role": "system",
                            "content": "If your code is a python script, then your code should not require any user "
                                       "input"},
                           {"role": "system",
                            "content": "The user is not using any notebook environment. You are forbidden to include "
                                       "any exclamation mark in the code"},
                           {"role": "system", "content": "Do not include any 'argparse' in the code"},
                           {"role": "system", "content": "Do not include any 'try or except' in the code"},
                           {"role": "system", "content": "Do not include any '__name__' in the code"},
                           ]

    def __init__(self, Input, Output, Objective, Privilege, Environment):
        self.Input = Input
        self.Output = Output
        self.Objective = Objective
        self.Privilege = Privilege
        self.Environment = Environment
        self.prompt_message = deepcopy(prompt_settings.base_prompt_message)
        self.prompt_message += [{"role": "system",
                                 "content": "The objective of the code is to " + self.Objective}]

    def action_type(self, Mode, combined_code, error, stdout, tb):
        if Mode == "Debug":
            self.prompt_message += [
                {"role": "system", "content": "The error message of the current code is:" + error},
                {"role": "system", "content": "The traceback of the exception is:" + tb},
                {"role": "user", "content": "Debug the code:" + combined_code + "The code should always include at "
                                                                                "least one function call inside it "
                                                                                "to demonstrate an execution. You "
                                                                                "should consider the error message:"
                                            + error}
            ]
        if Mode == "Improve":
            self.prompt_message += [
                {"role": "system", "content": "The standard output of the current code is:" + stdout},
                {"role": "user",
                 "content": "Improve the code:" + combined_code + f". The objective of the code is to {self.Objective}. "
                                                                  f"The code should always include at least one "
                                                                  f"function call inside it to demonstrate an "
                                                                  f"execution. If my code does not contain at least "
                                                                  f"one function call inside the code, you should "
                                                                  f"always add at least "
                                                                  f" one function call inside the code"},

                {"role": "system",
                 "content": "If my code does not contain at least one function call inside the code, you should "
                            "always add at least one function call inside the original code"}
            ]
        if Mode == "Create":
            self.prompt_message += [
                {"role": "user",
                 "content": f"Create the code for me. The objective of the code is to {self.Objective}. The code "
                            f"should always include at least one function call inside it to demonstrate an execution"}
            ]

        if Mode == "Killed":
            self.prompt_message += [
                {"role": "user",
                 "content": f"The code {combined_code} takes too long to run, modify the code so that it takes "
                            f"shorter time to finish. The objective of the code is to {self.Objective}."}
            ]

    def input_and_output_type(self):
        if self.Input is not None:
            self.prompt_message += [
                {"role": "system", "content": f"The input arguments given to the function call is: {self.Input}"}]

        if self.Output is not None:
            self.prompt_message += [
                {"role": "system",
                 "content": f"The standard output the python code should generate should be {self.Output}"}]

        if self.Privilege:
            self.prompt_message += [{"role": "system",
                                     "content": f"You can use any python packages. For example, you can use !pip install"}]
        else:
            self.prompt_message += {"role": "system", "content": "Do not include any 'pip install' in the code"}
            if self.Environment is None:
                self.prompt_message += [{"role": "system", "content": "The available python modules for the code "
                                                                      "only include the built-in python modules. The "
                                                                      "code in your generated response should not "
                                                                      "include any extra python packages"}]
            else:
                self.prompt_message += [{"role": "system","content": f"The available python modules for the code only "
                                                                     f"built-in python modules and the base_modules "
                                                                     f"in the list: {self.Environment}"}]


    def reset(self):
        self.prompt_message = deepcopy(prompt_settings.base_prompt_message)
        self.input_and_output_type()
