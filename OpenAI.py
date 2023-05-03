import openai
import time

openai.organization="org-2i9lWrQ8cRtI1wG0HtxcAV9e"
openai.api_key="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"

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

# Print the generated text
generated_text = response.choices[0].text
response_timestamp=time.time()
formatted_text = generated_text.replace(". ", ".\n")

prompt_length=len(prompt)
output_length=len(generated_text)

create_timestamp=response.get('created')
process_time=(response_timestamp-create_timestamp)
prompt_usage=response.get('usage').get('prompt_tokens')
completion_usage=response.get('usage').get('completion_tokens')
token_usage=response.get('usage').get('total_tokens')
prompt_ratio=round(prompt_length/prompt_usage,2)
output_ratio=round(output_length/completion_usage,2)
total_ratio=round((prompt_length+output_length)/token_usage,2)
tt_ratio=round(completion_usage/process_time,2)

##Some analytics
print(f'\nThe length of the prompt text is', prompt_length, 'characters.')
print(f'\nThe length of the output text is', output_length, 'characters.')
print(f'\nThe total cost of this this operation is', token_usage,'tokens; the prompt consumed', prompt_usage, 'tokens, while the',
        'output consumed', completion_usage, 'tokens.')
print(f'\nThe average prompt text length for one consumed prompt token is:', prompt_ratio, 'characters.')
print(f'\nThe average output text length for one consumed output token is:', output_ratio, 'characters.')
print(f'\nThe average total prompt + output text length for one consumed token is:', total_ratio, 'characters.')
print(f'\nHere is the answer to your question from ChatGPT:')
print(formatted_text)
print(f'\n\nThe processing time required to generate the response was', round(process_time,2), 'seconds')
print(f'\nThe ratio of tokens required to generate the response and the time (in seconds) taken to generate the response is', tt_ratio, 'tokens/second.')