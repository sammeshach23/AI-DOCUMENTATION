import streamlit as st
import pandas as pd
# from groq import Groq, APIConnectionError
from io import StringIO, BytesIO
import zipfile
import time
import google.generativeai as genai
import textwrap

# client = Groq(
#     api_key="",
# )

# openai.api_key = "your_openai_api_key"
GOOGLE_API_KEY = ""

genai.configure(api_key=GOOGLE_API_KEY)

st.title("AI Documentation Generator")
st.markdown("""
### Upload or Paste Your Code
This application will generate AI-powered documentation for your code.
Supports multiple programming languages like Python, C#, Java, edmx etc.
""")

uploaded_file = st.file_uploader("Upload a ZIP file containing your code", type=["zip"])
code_input = st.text_area("Or Paste Your Code Here:")

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def generate_documentation(code):
    prompt = (
        f"""Generate a comprehensive and well-structured documentation for the following project. 
        Analyze the workflow and relationships between the modules. Include explanations, function descriptions, 
        parameter details, and examples if applicable:
        \n\n{code}"""
    )
    for attempt in range(3):  
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            st.error(f"Connection error: {e}. Retrying...")
            time.sleep(2)  
    st.error("Failed to connect to the API after multiple attempts.")
    return None

def split_code_into_chunks(code, max_tokens=10000):
    lines = code.split('\n')
    chunks = []
    current_chunk = []
    current_length = 0

    for line in lines:
        line_length = len(line.split())
        if current_length + line_length > max_tokens:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_length = line_length
        else:
            current_chunk.append(line)
            current_length += line_length

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks

if st.button("Generate Documentation"):
    code_content = ""
    if uploaded_file:
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith(('.py', '.cs', '.java', '.cpp', '.js', '.edmx')):
                    with zip_ref.open(file_info) as file:
                        code_content += file.read().decode("utf-8") + "\n\n"
    elif code_input.strip():
        code_content = code_input
    else:
        st.error("Please provide code either by uploading a ZIP file or pasting it.")
        st.stop()
    
    st.markdown("### Generated Documentation:")
    chunks = split_code_into_chunks(code_content)
    documentation = ""
    for chunk in chunks:
        chunk_documentation = generate_documentation(chunk)
        if chunk_documentation:
            documentation += chunk_documentation + "\n\n"
    
    if documentation:
        st.markdown(documentation)
        st.download_button(
            label="Download Documentation",
            data=documentation,
            file_name="documentation.txt",
            mime="text/plain"
        )
