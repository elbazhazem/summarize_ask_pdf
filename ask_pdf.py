#Import our libraries
import os
import openai
import pdfplumber
from openai import OpenAI
from PIL import Image
from io import BytesIO
import streamlit as st


# Set your OpenAI API key   
os.environ["OPENAI_API_KEY"] = ""

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Extact text from PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

 # Summazie the text using OpenAI's GPT-3.5 Turbo model
def summarize_text(text):
    """Summarizes the text using OpenAI's latest API."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text: {text}"}
        ],
        max_tokens=300,
        temperature=0.7
    )
    # summary = response['choices'][0]['message']['content']
    summary = response.choices[0].message.content
    return summary

# Ask a question about the PDF file
def ask_question(text, question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about the provided text."},
            {"role": "user", "content": f"Please answer the following question based on the text:\n\n{text}\n\nQuestion: {question}"}
        ],
        max_tokens=300,
        temperature=0.7,
    )
    # answer = response['choices'][0]['message']['content']
    answer = response.choices[0].message.content.strip()
    return answer       

# Main function to process the PDF and answer questions
def main():
    st.title("Chat GPT AI - PDF Chatbot")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        if text:
            st.write("Text extracted from the PDF:")
            st.text_area("Extracted Text", text, height=150)
            
            # Show a summary of the text
            if st.button("Summarize Text"):
                summary = summarize_text(text)
                st.subheader("Summary:")
                st.write(summary)

            # Ask questions about the text
            question = st.text_input("Ask a question based on the text")
            if st.button("Get Answer"):
                answer = ask_question_about_text(text, question)
                st.subheader("Answer:")
                st.write(answer)
        else:
            st.error("No text could be extracted from this PDF.")

if __name__ == "__main__":
    main()
