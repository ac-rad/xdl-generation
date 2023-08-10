import os
import openai

from verify import verify_xdl


def prompt(instructions, description, max_tokens, model="text-davinci-003"):
    """Function that calls the OpenAI API"""
    if model == "text-davinci-003":
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
    
    elif model == "gpt-3.5-turbo" or model == "gpt-4":
        response = openai.ChatCompletion.create(
            model=model,
            messages = [
                {"role":"system", "content":"You are a natural language to XDL translator, you must also do your best to correct any incorrect XDL, only use items contained in the description, here is a description of XDL:\n"+description },
                {"role":"user", "content": f"\nConvert/Correct the following to proper XDL:\n{instructions}"}
            ],
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response["choices"][0]["message"]["content"]



def translate(input_xdl, model):
    """Function that translates the input XDL"""

    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai.organization = os.environ["OPENAI_ORGANIZATION_ID"]
    
    # Get XDL description
    with open("XDL_description.txt", "r") as f:
        XDL_description = f.read()

    correct_syntax = False
    errors = {}
    prev_input_xdl = input_xdl

    # Start 10 iteration for loop to limit token usage
    for step in range(10):
        print(f"Convert to XDL: {input_xdl}")
        try:
            gpt3_output = prompt(input_xdl, XDL_description, 1000, model)
        except:
            print("Error. Too many tokens required or invalid API key.")
            break

        if "<XDL>" in gpt3_output:
            gpt3_output = gpt3_output[gpt3_output.index("<XDL>"):gpt3_output.rindex("</XDL>") + 6]
            print(gpt3_output)
            print("gpt3_output:::")
            print(f"{gpt3_output}")
            compile_correct = verify_xdl(gpt3_output)
            errors[step] = {
                "errors": compile_correct,
                "input_xdl": input_xdl,
                "gpt3_output": gpt3_output,
            }
            if not compile_correct:
                correct_syntax = True
                break
            else:
                error_list = set()
                for item in compile_correct:
                    for error in item["errors"]:
                        error_list.add(error)
                error_message = f"\n{gpt3_output}\nThis XDL was not correct. These were the errors\n{os.linesep.join(list(error_list))}\nPlease fix the errors."
                input_xdl = f"{prev_input_xdl} {error_message}"

        else:
            error_message = f"\n{gpt3_output}\nThis XDL was not correct. XDL should start with <XDL> and end with </XDL>. Please fix the errors."
            input_xdl = f"{prev_input_xdl} {error_message}"

    try:
        if correct_syntax:
            xdl = gpt3_output
        else:
            xdl = "The correct XDL could not be generated."

    except Exception as e:
        print(f"Error: {e}")

    print(f"XDL: {xdl}")
    print(f"{xdl}")
    print(f"Final syntax valid: {correct_syntax}")