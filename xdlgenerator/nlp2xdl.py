import os
import openai
import sys
wd = os. getcwd()
root_dir = '/'.join(wd.split("/"))
print(wd.split("/"), root_dir)
sys.path.append(root_dir)
print(sys.path)
from verifier import verify
openai.api_key = os.environ["OPENAI_API_KEY"]

def prompt(instructions, description, max_tokens):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=description+instructions,
      temperature=0,
      max_tokens= max_tokens,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response["choices"][0]["text"]


instructions  = open("instructions.txt", "r").read()
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
    f = open("output_xdl.txt", "w")
    f.write(gpt3_output)
    f.close()
else:
    print("The correct XDL could not be generated.")
