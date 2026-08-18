import streamlit.components.v1 as components
import json


def speak(text):
    text = json.dumps(text)

    components.html(
        f"""
        <script>
            const text = {text};

            if ("speechSynthesis" in window) {{
                window.speechSynthesis.cancel();

                const speech = new SpeechSynthesisUtterance(text);

                speech.rate = 1.0;
                speech.pitch = 1.0;
                speech.volume = 1.0;

                window.speechSynthesis.speak(speech);
            }}
        </script>
        """,
        height=0
    )