# XDL-Generator

[![Run pytest](https://github.com/ac-rad/xdl-generation/actions/workflows/pytest.yml/badge.svg)](https://github.com/ac-rad/xdl-generation/actions/workflows/pytest.yml)

This repository contains
- LLM-based XDL generator
- XDL verifier

To generate a XDL protocol from a natural language description of an experiment, run the following: 

`python3 xdlgenerator/nlp2xdl.py --input_dir /path/to/experiment/dir` 

where `/path/to/experiment/dir` is a directory containing natural language experiments. Each experiment is assumed to be its own file in the dictory (e.g. expertiment1.txt, experiment2.txt). Running the script will automatically generate an output directory `/path/to/experiment/dir_output`. Each file in the new directory contains a XDL description. 
