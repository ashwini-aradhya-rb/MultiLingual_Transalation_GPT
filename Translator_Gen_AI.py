import streamlit as st
import openai
from gtts import gTTS
from io import BytesIO
import pandas as pd
import pdfplumber

# Set your OpenAI API key
openai.api_key = "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"

# Streamlit app configuration
st.title("Text Translator and Speech Synthesizer")
st.write("Translate text into different languages and convert it to speech.")

# Input text from the user
text_input = st.text_area("Enter the text you want to translate", height=200)

# PDF upload section
uploaded_file = st.file_uploader("Upload a PDF file")


def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            pages = pdf.pages
            text = ''.join(page.extract_text() for page in pages if page.extract_text())
        return text
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file)
        return df.to_string(index=False)
    elif file.name.endswith(".csv"):
        df = pd.read_csv(file)
        return df.to_string(index=False)
    return ""

# Extract text from the uploaded file if any
file_text = extract_text(uploaded_file) if uploaded_file else ""

# Select the target language
target_language = st.selectbox(
    "Select the target language",
    ["Kannada", "Hindi", "French", "Spanish", "German","Japanese"]
)

# Map languages to GPT-3 language codes
language_map = {
    "Kannada": "kn",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja"
}

# Translation button
if st.button("Translate and Convert to Speech"):
    if text_input or file_text :
        # Translate the text using GPT-3.5-turbo
        try:
            text = text_input+file_text
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
                ]
            )
            pass

            translated_text = response['choices'][0]['message']['content']
            st.success(f"Translated Text ({target_language}):")
            st.write(translated_text)

            # Convert the translated text to speech using gTTS
            tts = gTTS(translated_text, lang=language_map[target_language])

            # Save to a BytesIO object
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)

            # Play the audio in the app
            st.audio(audio_file, format="audio/mp3")

            # Download the audio file
            st.download_button(
                label="Download Audio",
                data=audio_file,
                file_name="translated_speech.mp3",
                mime="audio/mp3"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text to translate.")
