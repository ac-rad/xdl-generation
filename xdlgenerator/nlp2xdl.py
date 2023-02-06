import os
import openai
import sys
import argparse
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
    original_instructions = instructions
    correct_syntax = False
    for _ in range(100):
        gpt3_output = prompt(instructions, XDL, 2000)
        ## TO DO: input into checker
        print(gpt3_output)
        compile_correct = verify.verify_xdl(gpt3_output)
        if compile_correct:
            correct_syntax = True
            break
        else:
            error_message = "This XDL was not correct. These were the errors {}. Please fix the errors.".format(errors)
            instructions += original_instructions + " " + error_message
    if correct_syntax:
        return correct_syntax, gpt3_output
    else:
        return correct_syntax, "The correct XDL could not be generated."

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
        for filename in filenames:
            correct_syntax, xdl = generate_xdl(os.path.join(rootdir, filename))
            with open(os.path.join(output_dir, filename), "w") as f:
                f.write(xdl)
            total_num += 1
            num_correct += correct_syntax
    print("Total num correct:: {}".format(num_correct))
    print("Total num:: {}".format(total_num))

if __name__ == "__main__":
    main()
