# Introduction

MetaGPT is an application that automatically generates python codes based on GPT (as used
in ChatGPT).

While the naive GPT model (as used in ChatGPT) can generate Python codes, the code 
it generates often contains errors. Compared to the ChatGPT, MetaGPT tests the 
generated/managed codes locally and automatically ensures that the code can run 
smoothly and meet certain expectations.

MetaGPT combines metaprogramming (in Python) and large language models (LLMs) (GPT). 
* [Metaprogramming](https://en.wikipedia.org/wiki/Metaprogramming) refers to the 
programming method which involves one program (the meta program) writing another program
(the target program).
* [LLM](https://en.wikipedia.org/wiki/Large_language_model) are recently developed neural 
networks that can generate text based on the context.

Here is a simple illustration about our algorithm:

![alt text](https://github.com/JLX0/MetaGPT/blob/main/illustration.png?raw=true)

<hr/>

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
* This repository
```
git clone https://github.com/JLX0/MetaGPT.git
```
```
cd MetaGPT
```
* The OpenAI Python library (tested with 0.27.6)
```
pip install openai
```
<hr/>

* OpenAI API key with GPT-3.5 and/or GPT 4 access. You can get one from
[here](https://platform.openai.com/account/api-keys).

# Example usages

<hr/>

# Contributors

Jinglue Xu, Nagar Anthel Venkatesh Suryanarayanan, Ding Xia

Contact: jingluexu@gmail.com