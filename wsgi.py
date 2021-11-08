import sys

import cloudinary as Cloud
import cloudinary.uploader as cu
import os
from flask_cors import CORS, cross_origin
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from flask.json import jsonify
from flask import Flask, render_template, request, redirect
import caption_gen
# __name__ == __main__
app = Flask(__name__)
Cloud.config.update = (
                        { 'cloud_name' : os.environ.get('CLOUD_NAME'),
                        'api_key': os.environ.get('API_KEY'),
                        'api_secret': os.environ.get('API_SECRET')
                        })

@app.route('/')
def hello():
    return render_template("index.html")

# @app.route('/', methods = ['POST'])
# def marks():
#     if request.method == 'POST':
#         f = request.files['userfile']
#         path = "./static/{}".format(f.filename)
#         f.save(path)
#         caption = caption_gen.caption_this_image(path)
#         result_dic = {
#         'image' : path,
#         'caption' : caption
#         }
#     return render_template("index.html",your_result= result_dic)

@app.route('/', methods=['POST'])
def marks():
    # app.logger.info('in upload route')
    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['userfile']
        upload_result = cu.upload(file_to_upload)
        # print(upload_result)
        # app.logger.info('%s file_to_upload', file_to_upload)
        print(upload_result,file=sys.stderr)
        response = requests.get(upload_result["url"])
        img = Image.open(BytesIO(response.content))
        caption = caption_gen.caption_this_image(img)
        # app.logger.info(upload_result)
        result_dic = {
            'image': upload_result["url"],
            'caption': caption
        }
        return render_template("index.html", your_result=result_dic)


if __name__ == '__main__':
    app.debug = True
    app.run()

CORS(app)
