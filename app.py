import streamlit as st
from datetime import datetime
import random
from streamlit_geolocation import streamlit_geolocation
import requests
from core.speaker import speak

st.set_page_config(
    page_title="Jarvis Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------- Custom UI ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color: white;
}
.big {
    font-size:42px;
    font-weight:bold;
}
.card {
    background:#1f2937;
    padding:18px;
    border-radius:15px;
    border:1px solid #374151;
}
</style>
""", unsafe_allow_html=True)

location = streamlit_geolocation()
longitude = location['longitude'] if location else None
latitude = location['latitude'] if location else None

def get_weather(lat, lon):
    if lat is None or lon is None:
        return None
    api_key="c6c326ff2ff9b8f252c350b674ee305d"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    data = requests.get(url)
    
    
    return data.json()
# ---------- Memory ----------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------- Sidebar ----------
with st.sidebar:
    st.title("⚙️ Jarvis")
    st.write("Smart Assistant")
    if st.button("🗑 Clear Chat"):
        st.session_state.chat = []
    st.divider()
    st.write("**Quick Commands**")
    st.caption("hello")
    st.caption("time")
    st.caption("date")
    st.caption("weather")
    st.caption("joke")

# ---------- Header ----------
st.markdown('<p class="big">🤖 JARVIS</p>', unsafe_allow_html=True)
st.write("Your personal AI assistant built with Streamlit.")

# ---------- Chat History ----------
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

# ---------- Input ----------
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.chat.append(("user", prompt))

    text = prompt.lower()

    if "hello" in text:
        reply = "Hello sir ! Nice to meet you."
        speak("Hello sir ! Nice to meet you.")
    elif "time" in text:
        reply = f"Current time: **{datetime.now().strftime('%I:%M %p')}**"
        speak(f"Current time: **{datetime.now().strftime('%I %M %p')}")
    elif "date" in text:
        reply = f"Today's date is **{datetime.now().strftime('%d %B %Y')}**"
        speak(f"Today's date is **{datetime.now().strftime('%d %B %Y')}**")
    elif "weather" in text:
        weather= get_weather(latitude,longitude)
        if weather:
            city=weather["name"]
            temperature = weather["main"]["temp"]
        reply=f"the current weather in {city} is {temperature} degree Celsius"
        speak(f"the current weather in {city} is {temperature} degree Celsius")
         
    elif "joke" in text:
        reply = random.choice([
            "Why do programmers love Python? Because it's hiss-terical! 🐍",
            "I would tell you a UDP joke... but you might not get it.",
            "Debugging: Removing the needles from the haystack."
        ])
        speak(reply)
    elif "bye" in text or "exit" in text:
        reply=" Bye sir ! have a nice day"
        speak(reply)
    else:
        reply = f"You said: **{prompt}**"
        speak( f"You said: **{prompt}**")

    st.session_state.chat.append(("assistant", reply))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(reply)

# ---------- Footer ----------
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Messages", len(st.session_state.chat))
c2.metric("Status", "Online")
c3.metric("Version", "1.0")