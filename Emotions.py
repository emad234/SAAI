import os
import replicate
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

model_version = "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4"

# Define model + version

endpoint = "https://aistudioaiservices750088862480.cognitiveservices.azure.com/"
model_name = "gpt-4o"
deployment = "gpt-4o"

api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

filename = input("ENTER THE NAME OF THE IMAGE: ")
ImageType = input("ENTER PAINTING TYPE: ")
prompt = input("ENTER THE QUOTE: ")
response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "I will give you a quote from a person going through struggles. You have to list me the Emotions that the text conveys in the form of Keywords with no more descriptions just the emotions themselves. Give them all on one line. then on another line  HERE IS THE QUOTE" + prompt,
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)


prompt = response.choices[0].message.content
print(prompt)
response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt + "with this list of emotions provide me a list of detailied instructions MADE FOR AN IMAGE GENERATIVE AI on how to create a(n)" + ImageType + "art piece. specifiy everything from shape, color, textures, etc and make sure it captures the emotions perfectely and artisticly. Give them all on one line and with no extra words just instructions MADE FOR GENERATIVE AI",
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)
prompt = response.choices[0].message.content
print(prompt)


# Run the model
flag = 0
while not flag:
    try:    
        output = replicate.run(
            model_version,
            input={
                "prompt": "create a(n)" + ImageType + "art image while FOLLOWING THESE INSTRUCTIONS AS CLOSELY AS POSSIBLE:  " + prompt,
                "negative_prompt": "nudity, people, nsfw, inappropriate, blur"
            }
        )
        flag = 1
    except replicate.exceptions.ModelError:
        print("NSFW filter triggered. Retrying...")

print(output)  # this will print a list of image URLs

# Save image
import requests

image_url = output[0]

img_data = requests.get(image_url).content

with open(filename, 'wb') as handler:
    handler.write(img_data)

print("Image saved!")
