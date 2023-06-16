# Introduction

MetaLLM-GPT is an application that automatically generates Python codes based on GPT (as used
in ChatGPT).

While the naive GPT model (as used in ChatGPT) can generate Python codes, the code 
it generates often contains errors. When using ChatGPT to create Python codes,
you might find the code is unable to run due to various reasons (e.g., syntax errors).
Then you might try to manually debug it or ask ChatGPT again about how to fix it. If
you are tired of this repetitive process, MetaLLM-GPT is for you! Compared to ChatGPT, 
MetaLLM-GPT tests the generated/managed codes locally and automatically ensures that 
the code can run smoothly and meet certain expectations. 

Compared to [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT), MetaLLM-GPT is more
specialized in generating Python codes. By leveraging metaprogramming, MetaLLM-GPT is more
stable and easier to use.

Compared to [Smol developer](https://github.com/smol-ai/developer), MetaLLM-GPT is less focused on generating
the entire project but more focused on locally testing and debugging the generated code. In the future, we might
extend MetaLLM-GPT to generate the entire project or combine MetaLLM-GPT with Smol developer.

Compared to the [implicit code execution in Bard](https://blog.google/technology/ai/bard-improved-reasoning-google-sheets-export/),
MetaLLM-GPT was created independently at the same time or earlier. While Bard is great at using codes to assist 
responses from LLM, MetaLLM-GPT is great at using LLM to assist code generation. Also, MetaLLM-GPT allows for 
more complex code generation and execution, such as automatically installing packages, automatically debugging,
and using GPU.

MetaLLM-GPT combines metaprogramming (in Python) and large language models (LLMs) (GPT). 
* [Metaprogramming](https://en.wikipedia.org/wiki/Metaprogramming) refers to the 
programming method which involves one program (the meta program) reading/writing another 
program (the target program).
* [LLMs](https://en.wikipedia.org/wiki/Large_language_model) are recently developed neural 
networks that can generate text based on the context.



Here is a simple illustration of our algorithm:

![alt text](https://github.com/JLX0/MetaLLM-GPT/blob/main/illustration.png?raw=true)

On one hand, LLM is used as a tool that assists code generation. (see examples 1, 3, and 4). On the other hand, metaprogramming is used as a tool
for generating responses that complement LLM (see examples 2, 5, and 6). By combining the computational
power of Python codes and knowledge of GPT, MetaLLM-GPT demonstrates high versatility as an AI tool.

An easy-to-use __Google Colab version__ with examples is available 
[here](https://colab.research.google.com/drive/1TWN0mDmbdH1U2i85n7YUV9CKiRG0jJ9h?usp=sharing). The default settings
of the notebook use GPU instances, but you can run the notebook without GPU.

<hr>

# Installation and requirements

* Linux-based system (tested with Ubuntu 20.04 and 22.02)
* Python 3.7.1 or higher. We recommend using a new virtual environment 
(e.g., [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html))
```
conda create -n mg python=3.10
```
```
conda activate mg
```

* Pip. 

It is often already installed in most systems by default. You can check whether you have pip 
by running the following command:
```
which pip
```
If it is not installed, you can run the following command to install it:
```
sudo apt install python3-pip
```
or the following command if you are using a conda environment:
```
conda install pip
```

* This repository
```
git clone https://github.com/JLX0/MetaLLM-GPT.git
```
```
cd MetaLLM-GPT
```
* The OpenAI Python library (tested with 0.27.6)
```
pip install openai
```

* OpenAI API key with GPT-3.5 and/or GPT 4 access. You can get one from
[here](https://platform.openai.com/account/api-keys).

<hr/>

# Usage

## In general

Before using MetaLLM-GPT, please make sure that you have met the general requirements
as specified in *Installation and requirements*.

You can run the following command to check how to configure MetaLLM-GPT:
```
python3 mg.py -h
```

The file *mg.py* requires at least three arguments: *-o*, *-f*, and *-k*. 
* The argument *-o* describes the objective of this code
* The argument *-f* describes the path to the Python file that is supposed to be read 
and written by MetaLLM-GPT
* The argument *-k* describes the openAPI key you want to use

Please be careful about using a notebook format file (such as *.ipynb*) in *-f*, 
as GPT might try to execute Linux commands in the notebook.

If you want to use the *-e* argument (in order to create code beyond the built-in modules
in Python), it would be safer to download the required packages in the environment
beforehand.

If you want to use the *-p* argument (in order to let MetaLLM-GPT automatically install Python
packages), it is strongly recommended to run MetaLLM-GPT in a virtual environment with a 
pip inside the environment or with the [Google Colab version](https://colab.research.google.com/drive/1TWN0mDmbdH1U2i85n7YUV9CKiRG0jJ9h?usp=sharing). For example, if you use Conda, you can test whether there is a 
pip inside your environment by running the following command:
```
which pip
```

By default, MetaLLM-GPT assumes you want to use GPT 3.5. If you want to use GPT 4, please
set the argument *-g* to "4".


## For the following examples:
1. All of the following examples are available in [this Google Colab notebook](https://colab.research.google.com/drive/1TWN0mDmbdH1U2i85n7YUV9CKiRG0jJ9h?usp=sharing)
2. Please replace the key *"aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"* with your
own OpenAPI key. 

## Example 1: Generate a deep neural network using GPU

This command assumes that in your current environment, Pytorch is installed. If you prefer other deep
learning packages, please modify the *-e* arguments. The expected input of the neural network is the
batch size, learning rate, and training epochs. The expected output of the neural network is the 
validation accuracy of the model.

```
python3 mg.py -o "create a deep neural network that uses GPU" -f "DNN.py" -k "aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -in "1. bs: batch size 2. l:learning rate 3. e: training epochs " -out "the validation accuracy of the neural network" -e "1.pytorch" -l 300
```
The generated code is saved in your current working directory as a file named 
*dnn.py*. Sample codes generated by this command can be found in the folder *samples* (*dnn_1.py* and 
*dnn_2.py*)

The above commands assume that in your current environment, a GPU device is available to the Python packages. 
If not, please use the following command instead:

```
python3 mg.py -o "create a deep neural network that uses CPU" -f "DNN.py" -k "aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -in "1. bs: batch size 2. l:learning rate 3. e: training epochs " -out "the validation accuracy of the neural network" -e "1.pytorch" -l 300
```

## Example 2: Solve an undergraduate math problem

This example assumes that you have installed Sympy in your environment. You can set the *-p* argument as True to
let MetaLLM-GPT automatically install relevant packages. However, be careful with this option.

```
python3 mg.py -o "Consider the function f(x)=(x^3)((4x+5)^2), for what value of x is f'(x)=0" -f "math.py" -k "aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -out "values of x such that f'(x)=0" -e "1.sympy" -l 60
```

## Example 3: Generate audio from news websites

This example sets the *-p* argument as True, because the required packages are not commonly installed. It is advised
to set up a virtual environment for this example.

```
python3 mg.py -o "grab a news article from a news website, summarize the news article, then convert the summary into an audio" -f "news_audio.py" -k "aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -in "1.link. the link to the website of the news article. for example, it can be 'https://www.cnbc.com/2023/06/06/apple-ceo-tim-cook-says-ai-companies-need-to-regulate-themselves.html' 2. max_len. the maximum number of sentences in the summary." -out "the audio of the summary and the path to the audio file" -p True -l 300
```

## Example 4: Design a step in data processing

Due to the limitation of GPT, the length of the code generated by MetaLLM-GPT is usually limited to 150 lines.
In practice, many projects require codes of much higher length. However, MetaLLM-GPT can be still useful in such
situations because MetaLLM-GPT can be used to generate one step of the project at a time. For example, data preprocessing
and feature engineering in machine learning often involve a complex process. This example is a step that combines 
labels/outputs from three columns into one column.

```
python3 mg.py -o "There is a dataframe of three columns. Each column represents an output/label. Merge the three columns into one column such that each value in the new column is an integer that represents a distinct combination of the three values in the three columns" -f "data_process.py" -k "aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -in "1.df_raw. the dataframe with three columns" -out "the dataframe with the new column and the number of distinct values in the new column" -e "1.pandas" -l 60
```

## Example 5: Optimize a function

This example assumes that you have installed Scipy in your environment. You can set the *-p* argument as True to
let MetaLLM-GPT automatically install relevant packages. However, be careful with this option.


```
python3 mg.py -o "Optimize the following function f(x,y)=2*(x^2)-1.05*(x^4)+(x^6)/6+xy+y^2 by minimizing f(x,y)" -f "optimize.py" -k "aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -in "1. x. initial guesses of x 2. y. initial guesses of y" -out "the minimized f(x,y) and the values of x and y corresponds to the minimized value" -e 1.scipy -l 60
```

## Example 6: Draw a picture of a cat

This example assumes that you have installed Pillow in your environment. You can set the *-p* argument as True to
let MetaLLM-GPT automatically install relevant packages. However, be careful with this option.

The images generated by this method are quite simple and sometimes not recognizable, especially compared to 
those of the large generative models in computer vision. However, the images generated by this method are directly from 
Python codes. Moreover, the entire method (including LLM) does not require any training data with images in 
principle, which is an intriguing phenomenon.

```
python3 mg.py -o "Draw a picture of a cat" -f "draw.py" -k "aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -out "the image of the cat the path to the image file" -e 1.pillow -l 60
```

<hr/>

# Contributors

Jinglue Xu, Nagar Anthel Venkatesh Suryanarayanan, Ding Xia, Yossatong Road Tianlun, Zhen Liu, and Jianing, Qi

If you have any inquiries or want to collaborate with us, please contact us by 
emailing: jingluexu@gmail.com

If you like our project, please star our repository and share it with your friends!

<hr/>

# Citation

If you use any part of this code in your research, please cite our project:
```
@misc{Xu2023MetaLLMGPT,
  author = {Xu, Jinglue and Suryanarayanan, Nagar Anthel Venkatesh and Xia, Ding and Tianlun, Yossatong Road and Liu, Zhen and Qi, Jianing},
  title = {MetaLLM-GPT},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/JLX0/MetaLLM-GPT}},
  commit = {0f2cf89cdd153256a142939cedcdc58d7c4865e1}
}
```