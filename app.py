import streamlit as st
from openai import OpenAI
from io import BytesIO
import base64
import requests

st.set_page_config(page_title="Mandala Art Generator", layout="centered")
st.title("🌀 AI Mandala Generator")
st.markdown("Enter a **word**, and I’ll turn it into a black & white mandala!")

# Get API key securely from user
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# User inputs the word
user_word = st.text_input("🎨 Enter a word to generate mandala art", placeholder="e.g., peace")

# Submit button
if st.button("Generate Mandala"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not user_word:
        st.error("Please enter a word.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            prompt = f"A highly detailed, symmetrical black and white mandala illustration inspired by the word '{user_word}'. No color, only fine black lines on white background. Intricate, spiritual, and geometric."

            with st.spinner("Generating mandala..."):
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                image_url = response.data[0].url

                # Load image from URL
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_data = image_response.content

                    st.image(image_data, caption=f"Mandala inspired by '{user_word}'", use_column_width=True)

                    # Download button
                    b64 = base64.b64encode(image_data).decode()
                    href = f'<a href="data:image/png;base64,{b64}" download="mandala_{user_word}.png">📥 Download Mandala</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.error("Failed to fetch the image from OpenAI.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
