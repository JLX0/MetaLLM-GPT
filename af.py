import argparse
from af_core import AutoFunction

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--objective",
                    help='Describe the objective of this function. For example: "create a python code example using genetic algorithm"',
                    required=True)
parser.add_argument("-f", "--file_path", help='The path to the python file what is supposed to be read and written by AutoFunction. For example: "code.py". The file can include existing \
code, but it is advised to keep a seperate copy of your exisitng code.', required=True)
parser.add_argument("-in", "--input", help='The input arguments that should be included in the function. \
For example:"1.population_size: the size of the population, 2.max_generation: the number of generations the algorithm create"}',
                    default=None, type=None)
parser.add_argument("-out", "--output",
                    help='The output of the function. For example: "the fitness of the best individual"', default=None,
                    type=None)
parser.add_argument("-l", "--time_limit",
                    help='The time limit that each execution of the code can take in seconds. For example, 60.',
                    default=60,
                    type=int)
parser.add_argument("-e", "--environment", help='Describe the available python base_modules in your environment. \
For example: "1.numpy"', default=None, type=None)
parser.add_argument("-t", "--minimum_trial", help="The minimum number of iterations AutoFunction should try. Note that \
if the code is buggy or lacks output, then AutoFunction \
continues beyond the minimum number of iterations. For example: 10", default=10, type=int)
parser.add_argument("-r", "--resume",
                    help="Whether or not you already have an existing code and want to improve/debug based on it. For example: False",
                    default=False, type=bool)
parser.add_argument("-m", "--infinity_mode",
                    help="Whether or not you want AutoFunction to execute indefinitely until manual termination. For example: False",
                    default=False, type=bool)
parser.add_argument("-k", "--openapi_key", help='The openAPI key you want to use. If None, then a trial key is provided. For example: "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".\
To find your openAPI key, please check: https://platform.openai.com/account/api-keys',
                    default="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", type=str)
parser.add_argument("-v", "--verbose",
                    help="Whether or not you want to display additional information to debug AutoFunction. For example: False",
                    default=False, type=bool)

args = parser.parse_args()
config = vars(args)
print("Starting AutoFunction with the following configuration:", config)

af_instance = AutoFunction(Objective=config["objective"], File_path=config["file_path"],
                           Minimum_trial=config["minimum_trial"], Resume=config["resume"], Input=config["input"],
                           Output=config["output"], Time_limit=config["time_limit"], Environment=config["environment"],
                           Infinity_mode=config["infinity_mode"], Key=config["openapi_key"], Verbose=config["verbose"])
af_instance.run()
