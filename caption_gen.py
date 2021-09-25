#!/usr/bin/env python
# coding: utf-8

# In[1]:


from keras.layers import *
import re
import pickle
from time import time
import string
from keras.applications.vgg16 import VGG16
from keras.utils import to_categorical
from keras.layers.merge import add
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model, load_model
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.preprocessing import image
import numpy as np
import pandas as pd
import json


# In[2]:


model  = load_model('/Users/apoorvgarg/PycharmProjects/CB_lecture/ML_on_web/Image_Captioning/weights/model_9.h5')
#model._make_predict_function()

# In[3]:


model_temp = ResNet50(weights='imagenet',input_shape=(224,224,3))


# In[4]:


# Create a new model, by removing the last layer from the resnet 50


# In[5]:


model_resnet = Model(model_temp.input,model_temp.layers[-2].output)
#model_resnet._make_predict_function()

# In[9]:


def preprocess_image(img):
    img = image.load_img(img, target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img,axis=0)
    img = preprocess_input(img)
    return img


# In[27]:


def encode_image(img):
    img = preprocess_image(img)
    feature_vector = model_resnet.predict(img)
    feature_vector = feature_vector.reshape(1,feature_vector.shape[1])
    return feature_vector


# In[44]:


#enc = encode_image("Naruto.jpg")


# In[45]:


#enc.shape


# In[46]:


words_to_idx = {}
idx_to_words = {}


# In[47]:


with open('storage/word_to_idx.pkl','rb') as w2i:
    words_to_idx = pickle.load(w2i)  
    
with open('storage/idx_to_word.pkl','rb') as i2w:
    idx_to_words = pickle.load(i2w)  


# In[48]:


# words_to_idx


# In[49]:


def predict_caption(photo):
    in_text = 'startseq'
    max_len = 35
    for i in range(max_len):
        sequence = [words_to_idx[w] for w in in_text.split() if w in words_to_idx]
        sequence = pad_sequences([sequence],max_len,padding='post')
        
        y_pred = model.predict([photo,sequence])
        y_pred = y_pred.argmax() # word with max prob always. --> Greedy sampling
        word = idx_to_words[y_pred]
        in_text += (' ' + word)
        
        if word == 'endseq':
            break
            
        
    final_caption = in_text.split()[1:-1]
    final_caption = " ".join(final_caption)
    
    return final_caption


# In[50]:


#predict_caption(enc)


# In[ ]:

def caption_this_image(image):
    enc = encode_image(image)
    caption = predict_caption(enc)
    
    return caption



