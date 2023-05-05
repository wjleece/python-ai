import openai
import os

# Define the OpenAI model to be used
model = "gpt-3.5-turbo"
max_tokens = 1000


# Get org ID & API key from files
def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()


script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the script
org_id_file = os.path.join(script_dir, "org-id.txt")  # Construct the path to the org-id.txt file
api_key_file = os.path.join(script_dir, "api-key.txt")  # Construct the path to the api-key.txt file

openai.organization = read_file(org_id_file)
openai.api_key = read_file(api_key_file)

messages = [
    {"role": "system", "content": "You are a helpful assistant who answers questions\
If you think that a user may be finished with a set of questions, you can ask them if they have any further questions \
If they say yes, then continue helping them \
If they say no, then thank them and send an additional message of 'Interaction complete'"}]


# Make a request to the OpenAI API
def respond_to_messages(messages):
    response = openai.ChatCompletion.create(
        messages=messages,
        model=model,
        temperature=0.8
    )

    return response.choices[0].message["content"]


print("How can I help you? (Type 'quit' to exit)")
user_input = input("")  # Initial user request
messages.append({"role": "user", "content": user_input})  # append user request to messages


# The while loop below enables the interactivity between the user and the GPT assistant
# We stay in this while loop until either the user types 'quit'
# Or if the assistant determines that the conversation is over

def chat(user_input, messages):
    while user_input.lower() != "quit":
        if user_input.lower() == "quit":
            break
        response = respond_to_messages(messages)  # ChatGPT assistant's response initial user request
        messages.append({"role": "assistant", "content": response})  # append assistant response to messages
        if "Interaction complete" in response:
            break
        else:
            print(response)
        user_input = input("")  # User enters subsequent request
        messages.append({"role": "user", "content": user_input})  # add subsequent user request to conversation


if __name__ == "__main__":
    chat(user_input, messages)
