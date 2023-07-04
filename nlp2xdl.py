import json
import os
import sys

import numpy as np
import openai
from tqdm import tqdm
from flask_socketio import emit

wd = os.getcwd()
root_dir = "/".join(wd.split("/"))
sys.path.append(root_dir)
from verifier import verify



with open("static/config.json") as f:
    openai.api_key = json.load(f)["OPENAI_API_KEY"]


def prompt(instructions, description, max_tokens, task="\nConvert to XDL:\n", constraints=""):
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
        prompt=description + constraints + task + instructions,
        temperature=0,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]


def generate_xdl(file_path, socketio, available_hardware=None, available_reagents=None):
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
    task = "\nConvert to XDL:\n"

    constraints=""
    if available_hardware!= None:
        hardware_str = ", ".join(available_hardware)[:-2]
        constraints = f"\nThe available Hardware is: {hardware_str}\n"
    if available_reagents!= None:
        reagents_str = ", ".join(available_reagents)[:-2]
        constraints += f"\nThe available Reagents are: {reagents_str}\n"
    for step in range(10):
        socketio.emit("message", f"{constraints}\nConvert to XDL:\n{instructions}")
        try:
            gpt3_output = prompt(instructions, XDL, 1000, task, constraints)
        except:
             gpt3_output = prompt(instructions, XDL, 750, task, constraints)
        socketio.emit("message", "gpt3 output:::")
        socketio.emit("message_xdl", f"{gpt3_output}")
        print(f"output: {gpt3_output}")
        socketio.emit("message", "******")
        gpt3_output = gpt3_output[gpt3_output.index("<XDL>"):]
        compile_correct = verify.verify_xdl(gpt3_output, available_hardware, available_reagents)
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

    if correct_syntax:
        return correct_syntax, gpt3_output, errors
    else:
        return correct_syntax, "The correct XDL could not be generated.", errors


def main(input_dir, socketio, avail_hardware=None, avail_reagents=None):
    """main."""
    if input_dir[-1] == "/":
        input_dir = input_dir[:-1]
    output_dir = input_dir + "_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    available_hardware=None
    # if passed in avail hardware file, parse into list
    if avail_hardware != None:
        with open(avail_hardware) as f:
            available_hardware = f.read().split("\n")
    socketio.emit("message", f"available hardware: {available_hardware}")

    available_reagents=None
    # if passed in avail reagents file, parse into list
    if avail_reagents != None:
        with open(avail_reagents) as f:
            available_reagents= f.read().split("\n")
    socketio.emit("message", "available reagents: {available_reagents}")

    num_correct = 0
    total_num = 0
    for rootdir, subdirs, filenames in os.walk(input_dir):
        for ii, filename in tqdm(enumerate(sorted(filenames))):
            socketio.emit("message", filename)
            if ".txt" not in filename:
                continue
            try:
                correct_syntax, xdl, errors = generate_xdl(
                    os.path.join(rootdir, filename), socketio, available_hardware, available_reagents
                )
                socketio.emit("message", f"{xdl}")
                socketio.emit("correct_xdl", f"{xdl}")
                socketio.emit("message", f"{filename}\n{correct_syntax}")
                with open(os.path.join(output_dir, filename), "w") as f:
                    f.write(xdl)
                with open(os.path.join(output_dir, filename.replace(".txt", "_errors.json")),"w") as f:
                    json.dump(errors, f)
                total_num += 1
                num_correct += correct_syntax
            except Exception as e:
                socketio.emit("message", f"{e} {filename} error")
                continue
    
    socketio.emit("message", f"Total num correct:: {num_correct}")
    socketio.emit("message", f"Total num:: {total_num}")
    
