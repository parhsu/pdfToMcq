import openai
from services.fileManagement import read_pdf

# Set up the API key
# openai.api_key = secrets["api_key"]
openai.api_key = "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"
# model_engine = "davinci"
model_engine = "text-davinci-003"
# model_engine = "text-davinci-002"
# model_engine = "gpt-3.5-turbo"

pdf_text = read_pdf.read_all_pdf()

response = openai.Completion.create(
    engine=model_engine,
    prompt="make 5 question with 4 options with explanation from the data given " + pdf_text,
    # prompt="write an essay on independence day",
    max_tokens=2048,
    temperature=0.5,
    n=1
)

# Print the response
print(response.choices[0].text.strip())
print(response.choices)

result = ""
for choice in response.choices:
    result += choice.text

print(result)
