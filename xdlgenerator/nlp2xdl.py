import os
import json
import openai
import sys
import argparse
from tqdm import tqdm
wd = os. getcwd()
root_dir = '/'.join(wd.split("/"))
sys.path.append(root_dir)
from verifier import verify
openai.api_key = os.environ["OPENAI_API_KEY"]


def prompt(instructions, description, max_tokens):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=description+"\nConvert to XDL:\n"+instructions,
      temperature=0,
      max_tokens= max_tokens,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response["choices"][0]["text"]

def generate_xdl(file_path):
    instructions  = open(file_path, "r").read()
    XDL = open("XDL_description.txt", "r").read()
    prev_instr = instructions
    correct_syntax = False
    errors={}
    for step in range(10):
        gpt3_output = prompt(instructions, XDL, 2000)
        gpt3_output = gpt3_output[gpt3_output.index("<XDL>"):gpt3_output.index("</XDL>")+6]
        compile_correct = verify.verify_xdl(gpt3_output)
        errors[step] = {'errors': compile_correct, 'instructions': instructions, 'gpt3_output': gpt3_output}
        if len(compile_correct) == 0:
            correct_syntax = True
            break
        else:
            error_message = "This XDL was not correct. These were the errors {}. Please fix the errors.".format(compile_correct)
            instructions = prev_instr + " " + error_message

    if correct_syntax:
        return correct_syntax, gpt3_output, errors
    else:
        return correct_syntax, "The correct XDL could not be generated.", errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    args = parser.parse_args()
    if args.input_dir[-1] == "/":
        args.input_dir = args.input_dir[:-1]
    output_dir = args.input_dir + "_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    num_correct=0
    total_num=0
    for rootdir, subdirs, filenames in os.walk(args.input_dir):
        for ii, filename in tqdm(enumerate(sorted(filenames))):
            if ".txt" not in filename: 
                continue
            if ii == 1: continue
            correct_syntax, xdl, errors = generate_xdl(os.path.join(rootdir, filename))
            with open(os.path.join(output_dir, filename), "w") as f:
                f.write(xdl)
            with open(os.path.join(output_dir, filename.replace(".txt", "_errors.json")), 'w') as f:
                json.dump(errors, f)
            total_num += 1
            num_correct += correct_syntax
    print("Total num correct:: {}".format(num_correct))
    print("Total num:: {}".format(total_num))

if __name__ == "__main__":
    main()
