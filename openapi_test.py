import openai

# Set up the API key
# openai.api_key = secrets["api_key"]
openai.api_key = "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"
model_engine = "gpt-3.5-turbo"

models = openai.Model.list()

# print(models)

# print the first model's id
# create a completion
completion = openai.Completion.create(model="ada", prompt="Hello world")

# print the completion
print(completion.choices[0].text)


response = openai.Completion.create(
    engine=model_engine,
    prompt="make 5 question with 4 options with explanation from the data given  \n" + pdf_text,
    # prompt="write an essay on independence day",
    max_tokens=2048,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
