# Import required libraries
import streamlit as st
from PIL import Image
import io

import base64
import requests


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
# image_path = "/content/drive/MyDrive/YHCT_Data/test_2.jpg"
def process_image(image_path, api_key, user_input):
# Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"{user_input}"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 600
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']

def main():
    st.title("Image and Text Input App")

    st.sidebar.title("Open API Key")
    api_key = st.sidebar.text_input("Enter your API Key", type="password")
    
    # Create an image uploader
    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    # Create a text input field
    user_text = st.text_area("Enter your text here")

    if st.button("Submit"):
        if uploaded_image is not None and user_text:
            # Display the uploaded image
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            response = process_image(image, api_key, user_text)
            # Process the text with the model (assuming text generation for this example)
            # response = model(user_text)
            # response = [{'generated_text': 'pass'}]
            # Display the model response
            st.write("Model Response:")
            st.write(response)

if __name__ == "__main__":
    main()
