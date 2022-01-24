import json
import requests

from PIL import Image
from io import BytesIO

import caption_gen


class PythonPredictor:

    def __init__(self, config):
        pass

    def predict(self, payload):
        """
        sample input json:
        {
            "url": "https://tostpost.com/images/2018-Mar/23/04f023639327ba3a2e791fdd1c8ffdc7/1.jpg"
        }
        """
        image_url = payload["url"]
        image = requests.get(image_url).content
        img = Image.open(BytesIO(image))
        caption = caption_gen.caption_this_image(img)
        result_dic = {
            'image': image_url,
            'caption': caption
        }
        return json.dumps(result_dic)