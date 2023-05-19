from contextlib import redirect_stdout
import io
import traceback
import time
import argparse

import openai

parser = argparse.ArgumentParser()
                                 
parser.add_argument("-o", "--objective", help='Describe the objective of this function. For example: "create a python code example using genetic algorithm"',required=True)
parser.add_argument("-f", "--file_path", help='The path to the python file what is supposed to be read and written by AutoFunction. For example: "code.py". The file can include existing \
code, but it is advised to keep a seperate copy of your exisitng code.', required=True)
parser.add_argument("-in", "--input", help='The input arguments that should be included in the function. \
For example:"1.population_size: the size of the population, 2.max_generation: the number of generations the algorithm create"}',default=None,type=None)
parser.add_argument("-out", "--output", help='The output of the function. For example: "the fitness of the best individual"',default=None,type=None)
parser.add_argument("-e", "--environment", help='Describe the available python modules in your environment. \
For example: "1.numpy"',default=None,type=None)
parser.add_argument("-t", "--minimum_trial", help="The minimum number of iterations AutoFunction should try. Note that \
if the code is buggy or lacks output, then AutoFunction \
continues beyond the minimum number of iterations. For example: 10",default=10,type=int)
parser.add_argument("-r", "--resume", help="Whether or not you already have an existing code and want to improve/debug based on it. For example: False",default=False,type=bool)
parser.add_argument("-m", "--infinity_mode", help="Whether or not you want AutoFunction to execute indefinitely until manual termination. For example: False",default=False,type=bool)
parser.add_argument("-n", "--no_output", help="Whether or not a missing standard output from the python script is ok. For example: False",default=False,type=bool)
parser.add_argument("-k", "--openapi_key", help='The openAPI key you want to use. If None, then a trial key is provided. For example: "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".\
To find your openAPI key, please check: https://platform.openai.com/account/api-keys', default="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",type=str)
parser.add_argument("-v", "--verbose", help="Whether or not you want to display additional information to debug AutoFunction. For example: False",default=False,type=bool)

args = parser.parse_args()
config = vars(args)
print("Starting AutoFunction with the following configuration:", config)

openai.api_key=config["openapi_key"]

def find_string_in_the_middle(the_string):
    try:
        sub1="```python"
        idx1 = the_string.index(sub1)
    except:
        try:
            sub1="```"
            idx1 = the_string.index(sub1)
        except:
            sub1="``` python"
            idx1 = the_string.index(sub1)
    sub2="```"
    idx2 = the_string.index(sub2,idx1+1,)
    res = the_string[idx1 + len(sub1) + 1: idx2]
    return res

def run(Objective,File_path,Minimum_trial,Resume,Input=None, Output=None, Environment=None, Infinity_mode=False, No_output=False, Verbose=False):

    Resume=Resume
    
    trial_count=0
    
    result = False
    
    past_error_history=[]

    while True:
    
        try:
            
            print(f"---------Iteration {trial_count+1} starts!---------")
            trial_count+=1
            DEBUG=False
            
            if Resume==True:            
                file=open(File_path,"r")
                line_list = file.readlines()

                if Verbose:
                    print("raw string line by line:")
                    for line in line_list:
                        print(repr(line))
                        
                combined_code="".join(str(item) for item in line_list)

                if Verbose:
                    print("raw string combined:")
                    print("combined_list",repr(combined_code))
                try:
                    codeObject = compile(combined_code, 'sumstring_1', 'exec')
                except:
                    print("The compilation process failed")
                print("Testing the code by execting it...")
                
                stdout=None
                e=None
                current_global=list(globals().keys())
                
                if Verbose:
                    print("global variables before testing:",current_global)
                try:
                    f = io.StringIO()
                    with redirect_stdout(f):
                        exec(codeObject,globals())
                    stdout = f.getvalue()
                    print("The code runs smoothly")
                    if Output!=None and "save" not in combined_code and No_output==False:
                        if len(stdout)==0:
                            print("However, the code lacks a function call or valid output")
                        else:
                            print("Output of the code:\n"+stdout)
                except Exception as e:
                    error=str(e)
                    past_error_history.append(error)
                    tb=str(traceback.format_exc())
                    if e.__class__.__name__ == 'ModuleNotFoundError':
                        print("The generated code cannot be tested due to missing packages. It is advised to either change the objective, \
describe your current environment, or install the missing packages before proceeding with AutoFunction")
                        print("The error message is:",error)
                    else:
                        print("The code is buggy, debugging the code. The error message is:")
                        print(tb)
                    DEBUG=True
                
                total_global=list(globals().keys())
                if Verbose:
                    print("global variables after testing:",total_global)
                excessive_global=[x for x in total_global if x not in current_global]
                if Verbose:
                    print("excessive global variables:",excessive_global)
                for n in excessive_global:
                    del globals()[n]
                                    
            if DEBUG==False and trial_count > Minimum_trial and result== True and (len(stdout)!=0 or Output==None or "save" in combined_code or No_output==True) and Infinity_mode==False:
                break
                    
            if DEBUG==False:
                if (Resume==False and trial_count >1) or Resume==True:
                    print("Begin improving the code")
                else:
                    print("Begin creating the code")
            print("Thinking right now...")
            
            default_prompt_settings=[{"role": "system", "content": "You are a programming expert."},
                            {"role": "system", "content": "The code should always include at least one function call inside it to demonstrate an execution"},
                            {"role": "system", "content": "For your response, you should strictly follow the format ```python <python code that includes at least one function call to demonstrate an execution> ``` \
                            <Explanation about the generated code>"},
                            {"role": "system", "content": "You should always write all of the codes you generated in a single block. Any python codes in your response should always start with ```python and end with ```."},
                            {"role": "system", "content": "The objective of the code is to "+Objective},
                            {"role": "system", "content": "You should always include the full code in your response, instead of simply the modified part of the code or the function call."},
                            {"role": "system", "content": "You are forbidden to only include the modified part of the code in your response."},
                            {"role": "system", "content": "You are forbidden to only include the function call of the code in your response."},
                            {"role": "system", "content": "If your code is a python script, then your code should not require any user input"},
                            {"role": "system", "content": "The user is not using any notebook environment. You are forbidden to include any exclamation mark in the code"},
                            {"role": "system", "content": "Do not include pip install in the code"},
                            {"role": "system", "content": "Do not include argparse in the code"},
                            {"role": "system", "content": "Do not include try or except in the code"}
                            ]
                            
            if Input !=None:
                default_prompt_settings+=[{"role": "system", "content": f"The input arguments given to the function call is: {Input}"}]
                            
            if Output !=None:
                default_prompt_settings+=[{"role": "system", "content": f"The standard output the python code should generate should be {Output}"}]

            if Output !=None:
                default_prompt_settings+=[{"role": "system", "content": f"The available python modules for the code only include the built-in python modules and the modules in the list: {Environment}"}]
            else:
                default_prompt_settings+=[{"role": "system", "content": "The available python modules for the code only include the built-in python modules. The code in your generated response should not\
                include any extra python packages"}]
                
            if trial_count >1:
                current_start = time.time()               
                time_left=20-(current_start-previous_start)
                if time_left >=0:
                    time.sleep(time_left+0.1)
                                
            previous_start = time.time()

            if Resume:
                if DEBUG:
                    response=openai.ChatCompletion.create(
                      model="gpt-3.5-turbo",
                      messages=default_prompt_settings+[
                            {"role": "system", "content": "The error message of the current code is:"+error},
                            {"role": "system", "content": "The traceback of the exception is:"+tb},
                            {"role": "user", "content": "Debug the code:"+combined_code+" The code should always include at least one \
                            function call inside it to demonstrate an execution. You should consider the error message:"+error}
                        ]
                    )
                else:
                    response=openai.ChatCompletion.create(
                      model="gpt-3.5-turbo",
                      messages=default_prompt_settings+[
                            {"role": "system", "content": "The standard output of the current code is:"+stdout},
                            {"role": "user", "content": "Improve the code:"+combined_code+f". The objective of the code is to {Objective}. The code should always include at least one function call inside it to demonstrate an execution.\
                            If my code does not contain at least one function call inside the code, you should always add at least one function call inside the code"},
                            {"role": "system", "content": "If my code does not contain at least one function call inside the code, you should always add at least one function call inside the original code"}

                        ]
                    )
            else:
                response=openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=default_prompt_settings+[
                        {"role": "user", "content": f"Create the code for me. The objective of the code is to {Objective}. The code should always include at least one function call inside it to demonstrate an execution"}
                    ]
                )
                                   
            Resume=True
            
            response=response.choices[0].message.content

            print("modification during this iteration:\n", response)

            if Verbose:
                print("type of the raw response:",type(response))
                print("raw response:",repr(response))
            
            result = True
            
            if trial_count ==1:
                the_code=find_string_in_the_middle(response) 
            else:
                if len(find_string_in_the_middle(response)) >= 0.5*len(the_code):
                    the_code=find_string_in_the_middle(response)
                else:
                    print(f"---------Iteration {trial_count} failed!---------")
                    print("Reason of failure: the modified code is too short, change aborted")
                    result = False

            if Verbose:
                print("the generated code is",the_code)
            
            f = open(File_path, "w")
            f.write(the_code)
            f.close()
            
            print(f"---------Iteration {trial_count} succeeded!---------")
        except Exception as fail:
            result = False
            print(f"---------Iteration {trial_count} failed!---------")
            print("Reason of failure:", str(traceback.format_exc()))
        
    print("Done!")
        
run(config["objective"],config["file_path"],config["minimum_trial"],config["resume"],config["input"],config["output"],config["environment"],config["infinity_mode"],config["no_output"],config["verbose"])
