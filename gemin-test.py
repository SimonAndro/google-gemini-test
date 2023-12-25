import os
from dotenv import load_dotenv

load_dotenv()


import google.generativeai as genai 
import PIL.Image
import textwrap

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def pretty_print(text):
    text = text.replace('•', '  *')
    return (textwrap.indent(text, '> ', predicate=lambda _:True))

if __name__ == "__main__":

    img = PIL.Image.open("image.jpg")
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content(["write a poem that rhymes", img], stream=True)
    response.resolve()
    print(pretty_print(response.text))
    img.show()