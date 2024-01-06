import google.generativeai as genai
from openai import OpenAI

import requests
import json
import base64
import PIL.Image

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

website_info = {
    'website_type':  'business',
    'website_name':  'Neexa.AI',
    'website_decription': 'Neexa.AI is your AI-driven sales assistant, designed to address customer objections, negotiate and close deals on your behalf, — 24/7🚀',
}
generated_layout = ""


steps = {
    'generate-layout': {
        'prompt': f"Generate a responsive design layout for a {website_info['website_type']} website"
    },
    'generate-text': {
        'prompt': f"Generate text content for a {website_info['website_type']} website called {website_info['website_name']} with  description: {website_info['website_decription']}"
    },
    'generate-site': {
        'prompt': f"""use the provided website layout, text content and the pictures to generate a {website_info['website_type']} website for a {website_info['website_type']} website called {website_info['website_name']} with business description: {website_info['website_decription']}
        
        website layout: {generated_layout}"""
    }
}

def compress_image(input_path, output_path, quality=85):
    with PIL.Image.open(input_path) as img:
        img = img.resize((512,512))
        img.save(output_path, quality=quality)


if __name__ == "__main__":

    """
    image generation
    """
    image_prompts = [
        f"An image suitable for the welcome section of a {website_info['website_type']} website called {website_info['website_name']}, {website_info['website_decription']}.",
        f"An image suitable for the services or products section of a {website_info['website_type']} website called {website_info['website_name']}, {website_info['website_decription']}",
        f"A brand image suitable for a {website_info['website_type']} website called {website_info['website_name']}, {website_info['website_decription']}",
    ]
    client = OpenAI()

    count = 1
    for prompt in image_prompts:

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image = response.data[0]
        response = requests.get(image.url)

        with open(f"images/{count}.png", 'wb') as file:
            file.write(response.content)
        count = count+1

    # compress the images (they are quite large > 2MB)
    for count in range(1,4):
        compress_image(f"images/{count}.png",f"images/compressed/{count}.png")


    # """
    # website generation
    # """
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([
        f"Generate a well styled and responsive {website_info['website_type']} website for a {website_info['website_type']} website called {website_info['website_name']} with business description: {website_info['website_decription']}. Do not recite content from other sources.",
        PIL.Image.open("images/compressed/1.png"),
        PIL.Image.open("images/compressed/2.png"),
        PIL.Image.open("images/compressed/3.png")
    ])
    response.resolve()

    with open(f"website/index.html", 'w', encoding='utf-8') as file:
        for candidate in response.candidates:
            # file.write(response.candidates)
            print(candidate)
