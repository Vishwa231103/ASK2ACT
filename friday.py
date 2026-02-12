import os
import streamlit as st
from together import Together
import speech_recognition as sr
from gtts import gTTS
import tempfile

# ===========================
# 1. Setup
# ===========================
st.set_page_config(page_title="Friday - AI Voice Assistant", layout="centered")
st.title("🤖 Friday - Your AI Voice Assistant")

# Set Together AI API key
client = Together(api_key="22b64e2fb916b3509edc53e494ae373a3875f70bf9232b5ef9aa5385d65e587b")

# ===========================
# 2. Capture Speech
# ===========================
recognizer = sr.Recognizer()

def listen_speech():
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand."
        except sr.RequestError:
            return "Speech recognition service error."

# ===========================
# 3. Query Together AI API
# ===========================
def get_ai_response(user_input):
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": "You are Friday, an AI voice assistant. Always reply as if speaking directly to the user, friendly and helpful."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content

# ===========================
# 4. Convert AI Reply to Voice
# ===========================
def speak_text(text):
    # Add "Friday says" before speaking
    spoken_text = f"Friday says: {text}"
    tts = gTTS(text=spoken_text, lang="en")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)

    # Play audio inside Streamlit
    audio_file = open(tmp_file.name, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

# ===========================
# 5. Streamlit UI
# ===========================
if st.button("🎤 Talk to Friday"):
    user_text = listen_speech()
    st.subheader("You said:")
    st.write(user_text)

    if user_text and "sorry" not in user_text.lower():
        ai_reply = get_ai_response(user_text)
        st.subheader("🧠 Friday says:")
        st.write(ai_reply)

        speak_text(ai_reply)
