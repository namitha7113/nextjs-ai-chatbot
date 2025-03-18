# -*- coding: utf-8 -*-
"""Copy of Service_learning_NLP.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hAxg1i2ie5GU98jSiPpeNgMX-nd6s2VC
"""

pip install transformers sentencepiece torch
pip install flask

from flask import Flask, render_template, request, send_file
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
import nltk
from nltk.tokenize import sent_tokenize

# Initialize Flask app
app = Flask(__name__)

# Download required NLTK resources
nltk.download('punkt')

# Load the summarization model (T5-based)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Load the translation model (NLLB-200)
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate_text(text):
    """Function to translate English text to Kannada"""
    tokenizer.src_lang = "eng_Latn"
    sentences = sent_tokenize(text)
    translated_sentences = []

    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
        forced_bos_token_id = tokenizer.convert_tokens_to_ids("kan_Knda")

        with torch.no_grad():
            translated = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id)

        kannada_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
        translated_sentences.append(kannada_text)

    return " ".join(translated_sentences)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        english_text = uploaded_file.read().decode('utf-8')

        # Translate the full text
        translated_text = translate_text(english_text)

        # Summarize the text
        summarized_text = summarizer(english_text, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]

        # Translate the summarized text
        summarized_translated_text = translate_text(summarized_text)

        # Save the results to files
        translated_output_file = "static/kannada_translation.txt"
        summarized_output_file = "static/kannada_summarized_translation.txt"

        with open(translated_output_file, "w", encoding="utf-8") as file:
            file.write(translated_text)

        with open(summarized_output_file, "w", encoding="utf-8") as file:
            file.write(summarized_translated_text)

        return render_template('result.html',
                               translated_file=translated_output_file,
                               summarized_file=summarized_output_file)

    return "No file uploaded", 400

if __name__ == "__main__":
    app.run(debug=True)

# Install required libraries
!pip install -q transformers torch sentencepiece nltk

# Import necessary libraries
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from google.colab import files
import torch
import nltk

# Download required NLTK resources
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Load the summarization model (T5-based)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Load the translation model (NLLB-200)
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate_text(text):
    """Function to translate English text to Kannada"""
    tokenizer.src_lang = "eng_Latn"
    sentences = sent_tokenize(text)
    translated_sentences = []

    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
        forced_bos_token_id = tokenizer.convert_tokens_to_ids("kan_Knda")

        with torch.no_grad():
            translated = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id)

        kannada_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
        translated_sentences.append(kannada_text)

    return " ".join(translated_sentences)

# Upload the English text file
uploaded = files.upload()
input_file = list(uploaded.keys())[0]

# Read the English text from the file
with open(input_file, "r", encoding="utf-8") as file:
    english_text = file.read().strip()

# Translate the full text
translated_text = translate_text(english_text)

# Summarize the text
summarized_text = summarizer(english_text, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]

# Translate the summarized text
summarized_translated_text = translate_text(summarized_text)

# Save original translated text
translated_output_file = "kannada_translation.txt"
with open(translated_output_file, "w", encoding="utf-8") as file:
    file.write(translated_text)

# Save summarized and translated text
summarized_output_file = "kannada_summarized_translation.txt"
with open(summarized_output_file, "w", encoding="utf-8") as file:
    file.write(summarized_translated_text)

print("Translation and summarization completed! Download the output files below.")

# Provide files for download
files.download(translated_output_file)
files.download(summarized_output_file)

!apt install git

!git config --global user.name "YourGitHubUsername"
!git config --global user.email "your-email@example.com"