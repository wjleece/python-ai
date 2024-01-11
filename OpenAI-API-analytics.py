import openai
import os
import time


# Get org ID & API key from files
def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the script
org_id_file = os.path.join(script_dir, "org-id.txt")  # Construct the path to the org-id.txt file
api_key_file = os.path.join(script_dir, "api-key.txt")  # Construct the path to the api-key.txt file

openai.organization = read_file(org_id_file)
openai.api_key = read_file(api_key_file)


# Set up a prompt and model engine
prompt = input("\nAsk a question to ChatGPT here: ")
model = "gpt-4"


response = openai.ChatCompletion.create(
    model=model,
    messages=[{"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": prompt}],
    max_tokens=1000,
    temperature=0.8
)

# Print the response
response_text=response.choices[0].message['content'].strip()
response_text += '\n'
print(response_text)

# Get the response timestamp (not really sure if this is accurate)
response_timestamp = time.time()


# Calculate processing time (not really sure if this is accurate)
create_timestamp = response.get('created') # This is the request creation timestamp as reported by the OpenAI API
process_time = (response_timestamp - create_timestamp)

# Get input (prompt) and output text lengths
prompt_length = len(prompt)
output_length = len(response_text)

# Do some analytics
prompt_usage = response.get('usage').get('prompt_tokens')
completion_usage = response.get('usage').get('completion_tokens')
token_usage = response.get('usage').get('total_tokens')
prompt_ratio = round(prompt_length / prompt_usage, 2)
output_ratio = round(output_length / completion_usage, 2)
total_ratio = round((prompt_length + output_length) / token_usage, 2)
tt_ratio = round(completion_usage / process_time, 2)

# Print the output
print(f'\nThe length of the prompt text is', prompt_length, 'characters.')
print(f'\nThe length of the output text is', output_length, 'characters.')
print(f'\nThe total cost of this this operation is', token_usage, 'tokens; the prompt consumed', prompt_usage,
      'tokens, while the',
      'output consumed', completion_usage, 'tokens.')
print(f'\nThe average prompt text length for one consumed prompt token is:', prompt_ratio, 'characters.')
print(f'\nThe average output text length for one consumed output token is:', output_ratio, 'characters.')
print(f'\nThe average total prompt + output text length for one consumed token is:', total_ratio, 'characters.')
print(f'\nThe processing time required to generate the response was', round(process_time, 2), 'seconds')
print(
    f'\nThe ratio of tokens required to generate the response and the time (in seconds) taken to generate the '
    f'response is',
    tt_ratio, 'tokens/second.')
