from openai import OpenAI
from urllib.request import urlretrieve
from datetime import datetime
from .util import STATIC_PATH

def generate_image(prompt: str): 
    client = OpenAI()

    response = client.images.generate(
      model="dall-e-3",
      prompt="whatsapp-like sticker of" + prompt,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    image_url = response.data[0].url
    filename = str(int((datetime.now() - datetime(1970, 1, 1)).total_seconds())) + '.png'
    urlretrieve(image_url, STATIC_PATH + "fresh." + filename)

    return filename


