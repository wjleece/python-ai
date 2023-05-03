import openai
import time

# Replace with your organization's ID and API key
openai.organization = $org-id

# Get API key
# Create a file called api-key.txt and save your API key there
# This will prevent you from accidentally exposing your API key
def read_api_key(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the script
api_key_file = os.path.join(script_dir, "api-key.txt")  # Construct the path to the api-key.txt file

openai.api_key = read_api_key(api_key_file)

# Set up a prompt and model engine
prompt = input("\nAsk a question to ChatGPT here: ")
engine = "text-davinci-003"

# Make a request to the OpenAI API
response = openai.Completion.create(
    engine=engine,
    prompt=prompt,
    max_tokens=1000,
    n=1,
    stop=None,
    temperature=0.8,
)

# Parse the response
generated_text = response.choices[0].text

# Get the response timestamp (not really sure if this is accurate)
response_timestamp = time.time()

# Format the response
formatted_text = generated_text.replace(". ", ".\n")

# Get input (prompt) and output text lengths
prompt_length = len(prompt)
output_length = len(generated_text)

# Calculate processing time (not really sure if this is accurate)
create_timestamp = response.get('created')
process_time = (response_timestamp - create_timestamp)

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
print(f'\nHere is the answer to your question from ChatGPT:')
print(formatted_text)
print(f'\n\nThe processing time required to generate the response was', round(process_time, 2), 'seconds')
print(
    f'\nThe ratio of tokens required to generate the response and the time (in seconds) taken to generate the '
    f'response is',
    tt_ratio, 'tokens/second.')
