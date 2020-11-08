from flask import Flask, jsonify, request, render_template
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input,Dense,Dropout,LSTM,Embedding,GlobalMaxPooling1D
from tensorflow.keras.models import Model
import json
import pickle
app = Flask(__name__, template_folder='template')

from tensorflow.keras import layers

with open('/Trained Weights/Eminem_tokenizer.pkl', 'rb') as f:
    eminemTokenizer=pickle.load(f)
eminemVocab = eminemTokenizer.word_index

with open('/Trained Weights/Drake_tokenizer.pkl', 'rb') as f:
    drakeTokenizer=pickle.load(f)
drakeVocab = drakeTokenizer.word_index

with open('/Trained Weights/Kanye_tokenizer.pkl', 'rb') as f:
    kanyeTokenizer=pickle.load(f)
kanyeVocab = kanyeTokenizer.word_index

def create_eminem_model(num_heads,embedding_dim):
    i=Input(shape=(13,))
    x=Embedding(len(eminemVocab)+1,embedding_dim)(i)
    x=LSTM(512,return_sequences=True)(x)
    x=Dropout(0.2)(x)
    x=Dense(256,activation='relu')(x)
    x=GlobalMaxPooling1D()(x)
    x=Dense(len(eminemVocab)+1,activation='softmax')(x)
    model=Model(i,x)
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    return model
eminemModel = create_eminem_model(4,100)
eminemModel.load_weights('/Trained Weights/EminemRAPGmodel_LSTM.h5')

def create_drake_model(num_heads,embedding_dim):
    i=Input(shape=(15,))
    x=Embedding(len(drakeVocab)+1,embedding_dim)(i)
    x=LSTM(512,return_sequences=True)(x)
    x=Dropout(0.2)(x)
    x=Dense(256,activation='relu')(x)
    x=GlobalMaxPooling1D()(x)
    x=Dense(len(drakeVocab)+1,activation='softmax')(x)
    model=Model(i,x)
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    return model
drakeModel = create_drake_model(4,100)
drakeModel.load_weights('/Trained Weights/DrakeRAPGmodel_LSTM.h5')

def create_kanye_model(num_heads,embedding_dim):
    i=Input(shape=(15,))
    x=Embedding(len(kanyeVocab)+1,embedding_dim)(i)
    x=LSTM(512,return_sequences=True)(x)
    x=Dropout(0.2)(x)
    x=Dense(256,activation='relu')(x)
    x=GlobalMaxPooling1D()(x)
    x=Dense(len(kanyeVocab)+1,activation='softmax')(x)
    model=Model(i,x)
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    return model
kanyeModel = create_drake_model(4,100)
kanyeModel.load_weights('/Trained Weights/KanYeRAPGmodel_LSTM.h5')

def eminemPrediction(seed_text):
    next_words = 50
    for _ in range(next_words):
	    token_list = eminemTokenizer.texts_to_sequences([seed_text])[0]
	    token_list = pad_sequences([token_list], maxlen=13, padding='pre')
	    predicted = eminemModel.predict(token_list, verbose=0).argmax(axis=-1)
	    output_word = ""
	    for word, index in eminemTokenizer.word_index.items():
		    if index == predicted:
			    output_word = word
			    break
	    seed_text += " " + output_word
    return seed_text

def drakePrediction(seed_text):
    next_words = 50
    for _ in range(next_words):
	    token_list = drakeTokenizer.texts_to_sequences([seed_text])[0]
	    token_list = pad_sequences([token_list], maxlen=15, padding='pre')
	    predicted = drakeModel.predict(token_list, verbose=0).argmax(axis=-1)
	    output_word = ""
	    for word, index in drakeTokenizer.word_index.items():
		    if index == predicted:
			    output_word = word
			    break
	    seed_text += " " + output_word
    return seed_text

def kanyePrediction(seed_text):
    next_words = 50
    for _ in range(next_words):
	    token_list = kanyeTokenizer.texts_to_sequences([seed_text])[0]
	    token_list = pad_sequences([token_list], maxlen=15, padding='pre')
	    predicted = kanyeModel.predict(token_list, verbose=0).argmax(axis=-1)
	    output_word = ""
	    for word, index in kanyeTokenizer.word_index.items():
		    if index == predicted:
			    output_word = word
			    break
	    seed_text += " " + output_word
    return seed_text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/eminem')
def eminem():
    return render_template('eminem.html')

@app.route('/drake')
def drake():
    return render_template('drake.html')

@app.route('/kanye')
def drake():
    return render_template('kanye.html')

@app.route('/predict', methods=['POST'])
def predict():
    lmao = ""
    data = request.get_json(force = True)
    value=data['initialWords']
    artist = data['artist']
    if artist == "eminem":
        lmao = eminemPrediction(value)
    elif artist == "drake":
        lmao = drakePrediction(value)
    elif artist == "kanye":
        lmao = kanyePrediction(value)
    return jsonify(lmao)

if __name__ == "__main__":
    app.run(debug=True)