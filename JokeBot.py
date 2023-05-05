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
    {"role": "system", "content": "You are a helpful assistant \
A user will ask you to tell them a joke. You will respond with a question\
The user will tell you that they do not know the answer to your question \
You will then tell them an answer to the question that you asked that is humorous \
You must provide a humours answer to the question you asked \
Once you tell the joke, you should asked the user if they would like to hear another \
If they say yes, then tell another joke. If they say no then reply by saying 'Interaction complete'"}]


# Make a request to the OpenAI API
def respond_to_messages(messages):
    response = openai.ChatCompletion.create(
        messages=messages,
        model=model,
        temperature=0.8
    )

    return response.choices[0].message["content"]


def chat():
    print("How can I help you? (Type 'quit' to exit)")
    user_input = input("")  # Tell me a joke
    messages.append({"role": "user", "content": user_input})  # add 'Tell me a joke' user response to question
    while user_input.lower() != "quit":
        if user_input.lower() == "quit":
            break
        response = respond_to_messages(messages)  # ChatGPT's response to "Tell me a joke"
        messages.append({"role": "assistant", "content": response})  # ChatGPT's response is appended to messages
        # print(response)
        if "Interaction complete" in response:
            break
        else:
            print(response)
        user_input = input("")  # User answers the question to the joke
        messages.append({"role": "user", "content": user_input})  # add user response to question


chat()
