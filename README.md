# CLAIRify
## Errors are Useful Prompts: Instruction Guided Task Programming with Verifier-Assisted Iterative Prompting

- Project website: https://ac-rad.github.io/clairify/

This repository contains
- The source code for CLAIRify
- Dataset (Chem-RnD and Chem-EDU)
- CLAIRify web interface

### Tutorial
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ac-rad/xdl-generation/blob/master/tutorial.ipynb)

A tutorial on CLAIRify is provided as [Jupyter Notebook](https://github.com/ac-rad/xdl-generation/blob/master/tutorial.ipynb).

### Requirement
- OpenAI Python Library

You need to set your OpenAI API key in `OPENAI_API_KEY` environment variable.

### How to run
To generate a XDL protocol from a natural language description of an experiment, run the following: 

`python3 xdlgenerator/nlp2xdl.py --input_dir /path/to/experiment/dir` 

where `/path/to/experiment/dir` is a directory containing natural language experiments. Each experiment is assumed to be its own file in the dictory (e.g. expertiment1.txt, experiment2.txt). Running the script will automatically generate an output directory `/path/to/experiment/dir_output`. Each file in the new directory contains a XDL description.
