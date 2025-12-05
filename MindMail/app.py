# app.py
from flask import Flask, render_template, request
from offline_model import model_analyze
from audio_utils import record_audio, transcribe_audio
import re

app = Flask(__name__)

# Keyword fallback analyzer
def keyword_analyze(text):
    text_lower = text.lower()
    emotions = {
        "Happy 😀": ["happy", "joy", "glad", "cheerful", "delighted", "smile"],
        "Excited 🤩": ["excited", "thrilled", "awesome", "amazing", "stoked"],
        "Love ❤️": ["love", "affection", "like", "adore"],
        "Sad 😢": ["sad", "unhappy", "lonely", "depressed", "gloomy", "cry", "upset"],
        "Angry 😡": ["angry", "hate", "frustrated", "mad", "annoyed"],
        "Fear 😨": ["scared", "nervous", "fear", "anxious", "worried"],
    }
    for emotion, keywords in emotions.items():
        for w in keywords:
            if re.search(r'\b' + re.escape(w) + r'\b', text_lower):
                return emotion
    return "Neutral 😐"

@app.route("/", methods=["GET", "POST"])
def index():
    emotion = None
    mood_message = None
    background_class = "neutral-bg"
    user_message = ""

    if request.method == "POST":
        # If user clicked record button
        if "record_audio" in request.form:
            audio_file = record_audio(duration=5)
            user_message = transcribe_audio(audio_file)
        else:
            user_message = request.form.get("message", "")

        # Try offline HuggingFace model first
        try:
            emotion = model_analyze(user_message)
        except Exception as e:
            print("Model error:", e)
            emotion = keyword_analyze(user_message)  # fallback

        # Mood messages & background classes
        if "Happy" in emotion:
            mood_message = "Keep smiling! Take a moment to enjoy it!"
            background_class = "happy-bg"
        elif "Excited" in emotion:
            mood_message = "Awesome! Channel that energy positively!"
            background_class = "excited-bg"
        elif "Love" in emotion:
            mood_message = "Spread the love! Reach out to someone you care about!"
            background_class = "love-bg"
        elif "Sad" in emotion:
            mood_message = "Hope things get better soon. Listen to music or take a break."
            background_class = "sad-bg"
        elif "Angry" in emotion:
            mood_message = "Take a deep breath. Step away and relax for a bit."
            background_class = "angry-bg"
        elif "Fear" in emotion:
            mood_message = "Stay calm, you got this. Try deep breathing or meditation."
            background_class = "fear-bg"
        elif "Confused" in emotion:
            mood_message = "Take your time. Maybe write down your thoughts or ask for help."
            background_class = "confused-bg"
        elif "Tired" in emotion:
            mood_message = "Rest well. A short nap or break might help."
            background_class = "tired-bg"
        else:
            mood_message = "Feeling neutral. Keep going!"
            background_class = "neutral-bg"

    return render_template(
        "index.html",
        emotion=emotion,
        mood_message=mood_message,
        background_class=background_class,
        user_message=user_message
    )

if __name__ == "__main__":
    app.run(debug=True)
