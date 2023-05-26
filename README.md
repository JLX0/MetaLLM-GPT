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



<hr/>

