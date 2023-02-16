#from verifier import verify
import argparse
import json
import os
import sys

import numpy as np
import openai
from tqdm import tqdm

wd = os.getcwd()
root_dir = "/".join(wd.split("/"))
sys.path.append(root_dir)
from verifier import verify

openai.api_key = os.environ["OPENAI_API_KEY"]


def prompt(instructions, description, max_tokens, task="\nConvert to XDL:\n"):
    """prompt.

    Parameters
    ----------
    instructions :
        instructions
    description :
        description
    max_tokens :
        max_tokens
    task :
        task
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=description + "\nConvert to XDL:\n" + instructions,
        temperature=0,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]


def generate_xdl(file_path):
    """generate_xdl.

    Parameters
    ----------
    file_path :
        file_path
    """
    instructions = open(file_path, "r").read()
    XDL = open("XDL_description.txt", "r").read()
    prev_instr = instructions
    correct_syntax = False
    errors = {}
    #error_list = set()
    task = "\nConvert to XDL:\n"
    for step in range(10):
        print(instructions)
        gpt3_output = prompt(instructions, XDL, 1000, task)
        print(gpt3_output)
        gpt3_output = gpt3_output[gpt3_output.index("<XDL>"):]
        # gpt3_output = gpt3_output[gpt3_output.index("<XDL>"):gpt3_output.index("</XDL>")+6]
        compile_correct = verify.verify_xdl(gpt3_output)
        #    error_list = set()
        # for ii in compile_correct:
        #    for jj in ii['errors']:
        #        error_list.add(jj)
        # error_list += compile_correct
        errors[step] = {
            "errors": compile_correct,
            "instructions": instructions,
            "gpt3_output": gpt3_output,
        }
        if len(compile_correct) == 0:
            correct_syntax = True
            break
        else:
            error_list = set()
            for ii in compile_correct:
                for jj in ii["errors"]:
                    error_list.add(jj)
            abl=2
            if abl== 0:
                error_message = "\n{}\nThis XDL was not correct. Please fix the errors.".format(
                    gpt3_output
                )
            elif abl==1:
                error_message = "These are XDL errors.\n{}\nPlease fix the errors.".format(
                    "\n".join(list(error_list))
                )
            #### BEST ONE:
            elif abl==2:
                error_message = "\n{}\nThis XDL was not correct. These were the errors\n{}\nPlease fix the errors.".format(
                    gpt3_output,
                    "\n".join(list(error_list))
                )
            instructions = prev_instr + " " + error_message
            # instructions = prev_instr + " " + error_message
            # task = ''
            # task = f"\nOriginal instructions:\n{prev_instr}\nFix this XDL:\n"
            # task = "\nFix this XDL:\n"

    if correct_syntax:
        return correct_syntax, gpt3_output, errors
    else:
        return correct_syntax, "The correct XDL could not be generated.", errors


def main():
    """main."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    args = parser.parse_args()
    if args.input_dir[-1] == "/":
        args.input_dir = args.input_dir[:-1]
    output_dir = args.input_dir + "_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    num_correct = 0
    total_num = 0
    for rootdir, subdirs, filenames in os.walk(args.input_dir):
        np.random.seed(42)
        np.random.shuffle(filenames)
        filenames_subset = filenames[:125]
        for ii, filename in tqdm(enumerate(sorted(filenames_subset))):
            print(filename)
            if os.path.exists(os.path.join(output_dir, filename)):
                continue
            if ".txt" not in filename:
                continue
            if True:  # try:
                correct_syntax, xdl, errors = generate_xdl(
                    os.path.join(rootdir, filename)
                )
                print(filename, correct_syntax)
                with open(os.path.join(output_dir, filename), "w") as f:
                    f.write(xdl)
                with open(
                    os.path.join(output_dir, filename.replace(
                        ".txt", "_errors.json")),
                    "w",
                ) as f:
                    json.dump(errors, f)
                total_num += 1
                num_correct += correct_syntax
            if False:  # except:
                print(filename, "error")
                continue
    print(f"Total num correct:: {num_correct}")
    print(f"Total num:: {total_num}")


if __name__ == "__main__":
    main()
