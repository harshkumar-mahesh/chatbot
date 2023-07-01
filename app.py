from flask import Flask, render_template, request

# Import the required code from your Python script
import pandas as pd
import numpy as np
import openai
import nltk
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# Load the API key from the file
API_KEY = open("api_key.txt", "r").read()
openai.api_key = API_KEY

df = pd.read_csv('clean_data.csv')

# Functions from the Python script

def convert_to_base_form(sentence):
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(sentence)
    base_words = [lemmatizer.lemmatize(word) for word in words]
    base_sentence = ' '.join(base_words)
    return base_sentence

def find_word_index(sentence, word_array):
    sentence_words = sentence.lower().split()
    for i, word in enumerate(word_array):
        if word.lower() in sentence_words:
            return i
    return -1

def retrieve_row_info(df, index):
    row_info = []
    if index != -1:
        for column in df.columns:
            value = df.loc[index, column]
            row_info.append(f"{column}: {value}")
        return '\n'.join(row_info)
    else:
        return "None"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    base_form = convert_to_base_form(user_message)
    word_index = find_word_index(base_form, food_items)
    info = retrieve_row_info(df, word_index)
    
    if info != 'None':
        user_message = user_message + " give some information about the food item mentioned here like two or three lines and also display these values as list: '"+info+"'"
    
    if user_message.lower() == "quit":
        return "Thank you for your time."

    chat_log.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
    )
    assistant_response = response['choices'][0]['message']['content']
    chat_log.append({"role": "assistant", "content": assistant_response.strip("\n").strip()})
    
    return assistant_response.strip("\n").strip()


if __name__ == '__main__':
    # Extract first word(s) from the 'Text' column
    df['First_Word'] = df['Food and Serving'].str.split().str[0]

    food_items = df['First_Word'].values
    # Remove the comma from each element in the array
    food_items = [element.replace(',', '') for element in food_items]
    # Convert all elements to lowercase
    food_items = [element.lower() for element in food_items]

    chat_log= []

    app.run()
