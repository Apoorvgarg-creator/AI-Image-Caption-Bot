import sys
import cloudinary as Cloud
import cloudinary.uploader as cu
import os
from requests import get as rq
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request, redirect
import caption_gen

app = Flask(__name__)
Cloud.config.update = (
                        { 'cloud_name' : os.environ.get('CLOUD_NAME'),
                        'api_key': os.environ.get('API_KEY'),
                        'api_secret': os.environ.get('API_SECRET')
                        })

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def marks():
    if request.method == 'POST':
        file_to_upload = request.files['userfile']
        upload_result = cu.upload(file_to_upload)
        response = rq(upload_result["url"])
        img = Image.open(BytesIO(response.content))
        caption = caption_gen.caption_this_image(img)
        result_dic = {
            'image': upload_result["url"],
            'caption': caption
        }
        return render_template("index.html", your_result=result_dic)

if __name__ == '__main__':
    app.debug = True
    app.run()

