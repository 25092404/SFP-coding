import streamlit as st
import time
import random
from datetime import datetime
import os
import json
import google.generativeai as genai

# --- Configure Gemini ---
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your real key
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Alarm sound using HTML5 audio ---
def play_alarm_html():
    st.markdown(
        """
        <audio autoplay loop id="alarm-audio">
            <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
            Your browser does not support the audio element.
        </audio>
        """,
        unsafe_allow_html=True
    )

def stop_alarm_html():
    st.markdown(
        """
        <script>
            var audios = document.querySelectorAll("audio");
            audios.forEach(audio => audio.pause());
        </script>
        """,
        unsafe_allow_html=True
    )

# --- Daily completion logging for prize eligibility ---
def log_success():
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = "alarm_log.json"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[today] = True
    with open(log_file, "w") as f:
        json.dump(data, f)

def check_monthly_completion():
    log_file = "alarm_log.json"
    if not os.path.exists(log_file):
        return 0
    with open(log_file, "r") as f:
        data = json.load(f)
    current_month = datetime.now().strftime("%Y-%m")
    return sum(1 for day in data if day.startswith(current_month))

# --- Streamlit UI ---
st.set_page_config(page_title="Smart Alarm", page_icon="⏰")
st.title("⏰ Smart Alarm Clock Challenge")

alarm_time = st.time_input("Set Your Alarm Time")
category = st.selectbox("Choose Your Wake-Up Challenge", ["Math Question", "Mirror Selfie"])
activate = st.button("Activate Alarm")

if activate:
    st.success(f"✅ Alarm set for {alarm_time.strftime('%H:%M:%S')}")
    waiting_placeholder = st.empty()

    # Wait until the alarm time
    while True:
        now = datetime.now().time()
        if now >= alarm_time:
            play_alarm_html()
            break
        remaining = datetime.combine(datetime.today(), alarm_time) - datetime.now()
        waiting_placeholder.info(f"⏳ Waiting for alarm... Time left: {str(remaining).split('.')[0]}")
        time.sleep(1)

    st.warning("🚨 WAKE UP! Complete the challenge to stop the alarm.")

    # Challenge 1: Math
    if category == "Math Question":
        mistake_count = 0
        num1 = random.randint(10, 99)
        num2 = random.randint(1, 10)
        operator = random.choice(["+", "-", "*", "//"])
        question = f"{num1} {operator} {num2}"
        correct_answer = eval(question)

        st.subheader("📘 Solve this:")
        st.markdown(f"**{question} = ?**")
        user_answer = st.number_input("Your Answer:", step=1)
        check_answer = st.button("Submit Answer")

        if check_answer:
            if user_answer == correct_answer:
                stop_alarm_html()
                log_success()
                st.success("✅ Correct! Alarm stopped.")
                st.balloons()
            else:
                mistake_count += 1
                st.error(f"❌ Incorrect! Mistake {mistake_count}/3")
                if mistake_count >= 3:
                    st.info(f"The correct answer was: **{correct_answer}**")
                    stop_alarm_html()
                    log_success()

    # Challenge 2: Mirror Selfie
    elif category == "Mirror Selfie":
        st.subheader("📸 Upload your Mirror Selfie:")
        uploaded_file = st.file_uploader("Upload a picture to stop the alarm", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            stop_alarm_html()
            log_success()
            st.success("✅ Selfie uploaded. Alarm stopped.")
            st.image(uploaded_file, use_column_width=True)
            st.balloons()

    # Show prize eligibility progress
    completed_days = check_monthly_completion()
    st.info(f"📅 You’ve completed the challenge on **{completed_days}** day(s) this month.")
    if completed_days >= 30:
        st.success("🎉 You are eligible for the RM200 monthly lucky draw!")
