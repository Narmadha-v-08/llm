import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv('sk-proj-kKDuy8RdIhiaYtCSHW4kT3BlbkFJTVWNVK9rXCSKrV1QNsab')

# Function to generate the inspection report
def generate_inspection_report(inspection_data):
    prompt = f"Generate a detailed inspection report based on the following data: {inspection_data}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text

# Function to provide recommendations
def get_recommendations(inspection_data):
    prompt = f"Provide recommendations for the following inspection data: {inspection_data}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text

# Function to translate reports
def translate_report(report, target_language):
    prompt = f"Translate the following report to {target_language}: {report}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text

# Streamlit UI
st.title('Vehicle Inspection App')

# Text area for inspection data input
inspection_data = st.text_area("Enter inspection data:")

# Button to generate report
if st.button('Generate Report'):
    report = generate_inspection_report(inspection_data)
    st.subheader("Inspection Report")
    st.write(report)

    # Provide recommendations
    recommendations = get_recommendations(inspection_data)
    st.subheader("Recommendations")
    st.write(recommendations)

    # Translation options
    language = st.selectbox("Translate report to:", ["None", "Spanish", "French", "Hindi"])
    if language != "None":
        translated_report = translate_report(report, language)
        st.subheader(f"Translated Report ({language})")
        st.write(translated_report)
