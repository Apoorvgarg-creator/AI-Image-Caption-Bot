import pickle
import sys
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np

model = load_model('weights/model_9.h5')
model_temp = ResNet50(weights='imagenet',input_shape=(224,224,3))
model_resnet = Model(model_temp.input,model_temp.layers[-2].output)

def preprocess_image(img):
    print(img,file=sys.stderr)
    target_size = (224, 224)
    img = img.resize(target_size)
    img = image.img_to_array(img)
    img = np.expand_dims(img,axis=0)
    img = preprocess_input(img)
    return img

def encode_image(img):
    img = preprocess_image(img)
    feature_vector = model_resnet.predict(img)
    feature_vector = feature_vector.reshape(1,feature_vector.shape[1])
    return feature_vector

words_to_idx = {}
idx_to_words = {}

with open('storage/word_to_idx.pkl','rb') as w2i:
    words_to_idx = pickle.load(w2i)  
    
with open('storage/idx_to_word.pkl','rb') as i2w:
    idx_to_words = pickle.load(i2w)  

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

def caption_this_image(image):
    enc = encode_image(image)
    caption = predict_caption(enc)
    
    return caption



