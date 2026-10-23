
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🖼️",
    layout="centered"
)

st.title("🖼️ AI Image Caption Generator")
st.write(
    "Upload an image to generate a meaningful caption "
    "and understand the objects and scenes in it."
)

api_key = os.getenv("GEMINI_API_KEY")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image",
             use_container_width=True)

    if st.button("Generate Caption"):
        if not api_key:
            st.error("API key missing. Please check your .env file.")
        else:
            try:
                client = genai.Client(api_key=api_key)

                image_part = types.Part.from_bytes(
                    data=uploaded_file.getvalue(),
                    mime_type=uploaded_file.type
                )

                prompt = """
                Analyze this image carefully.

                1. Image Caption: Write a clear, meaningful caption
                   describing the image.
                2. Objects Detected: List the main visible objects.
                3. Scene Explanation: Explain what is happening
                   in the image and describe its setting.

                Only describe details that are reasonably visible.
                Do not guess unknown information.
                """

                with st.spinner("Analyzing image..."):
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[prompt, image_part]
                    )

                st.subheader("✨ Generated Caption and Analysis")
                st.markdown(response.text)

            except Exception as e:
                st.error("Could not analyze the image.")
                st.write(str(e))
