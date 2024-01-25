import json
import openai
import speech_recognition as sr
from gtts import gTTS
import os

# Load API keys
with open('api_keys.json') as f:
    api_keys = json.load(f)

# Set up GPT-3 API key
openai.api_key = api_keys["gpt3"]

# Set up Speech Recognition
recognizer = sr.Recognizer()

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save('response.mp3')
    os.system('start response.mp3')

# Function to interact with GPT-3
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Main loop
while True:
    # Get user input through speech
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        user_input = recognizer.recognize_google(audio)
        print("You said:", user_input)

        # Use GPT-3 to generate a response
        gpt_response = chat_with_gpt(user_input)
        print("GPT-3 Response:", gpt_response)

        # Convert GPT-3 response to speech and play it
        text_to_speech(gpt_response)

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
    except sr.RequestError as e:
        print(f"Speech recognition request failed: {e}")
