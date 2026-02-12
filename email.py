import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from openai import OpenAI
import playsound
import tempfile
import time
import os

# ---------------- SETUP ----------------
st.set_page_config(page_title="Friday AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Friday - Your Talking AI Assistant")
st.write("Speak or type to chat with your personal AI — Friday!")

# ✅ Add your OpenAI API key here
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # Replace with your real key

# ---------------- FUNCTIONS ----------------

# 🎤 Listen to your voice
def listen_to_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... please speak now.")
        audio = r.listen(source, phrase_time_limit=8)
    try:
        query = r.recognize_google(audio, language="en-in")
        return query
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Network issue. Please check your internet connection."

# 🧠 Get AI reply using GPT model
def ai_reply(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # GPT-4 optimized model (fast and smart)
            messages=[
                {"role": "system", "content": "You are Friday, a helpful and friendly female AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"

# 🔊 Speak the reply using Google TTS
def speak_text(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang='en', tld='co.in')
            tts.save(fp.name)
            temp_path = fp.name

        time.sleep(0.5)  # Give Windows time to release the file
        playsound.playsound(temp_path)
        os.remove(temp_path)
    except Exception as e:
        st.error(f"TTS Error: {e}")

# ---------------- STREAMLIT UI ----------------

st.divider()
col1, col2 = st.columns(2)

# 🎙️ Voice Input Button
if col1.button("🎤 Talk to Friday"):
    user_query = listen_to_user()
    st.write(f"🗣️ You said: **{user_query}**")

    reply = ai_reply(user_query)
    st.write(f"🤖 Friday: {reply}")

    speak_text(reply)

# 💬 Text Input
user_input = st.text_input("💬 Or type your message below:")
if col2.button("Send"):
    if user_input.strip():
        reply = ai_reply(user_input)
        st.write(f"🤖 Friday: {reply}")
        speak_text(reply)
    else:
        st.warning("Please enter something first.")

st.divider()
st.caption("Developed with ❤️ by Karthik’s AI Friday")
