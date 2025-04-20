import streamlit as st
from streamlit_extras.colored_header import colored_header

import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from langdetect import detect
from googletrans import Translator

st.set_page_config(layout="wide")

def extractive_summary(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()  
    summary = summarizer(parser.document, num_sentences)
    return ' '.join(str(sentence) for sentence in summary)

@st.cache_resource
def text_summary(text, method="abstractive", limit=None):
    if method == "abstractive":
        summary = Summary()
        result = summary(text)
    elif method == "extractive":
        result = extractive_summary(text, limit)
    return result

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:  
            text += page.extract_text() if page.extract_text() else ""
    return text

def detect_language(text):
    return detect(text)

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Add app logo


# Add colored header
colored_header(
    "Streamlit Text Summarization App",
    description="Summarize text or documents using different techniques",
    color_name="red-70"
)

choice = st.sidebar.radio("Select your choice", ["Summarize Text", "Summarize Document"], horizontal=True)
summarization_type = st.sidebar.radio("Choose summarization type", ("Abstractive", "Extractive"), horizontal=True)

if "summary_result" not in st.session_state:
    st.session_state.summary_result = ""
if "translated_summary" not in st.session_state:
    st.session_state.translated_summary = ""
if "translated_input" not in st.session_state:
    st.session_state.translated_input = ""

if choice == "Summarize Text":
    colored_header("Summarize Text using txtai", color_name="blue-70")
    input_text = st.text_area("Enter your text here")

    num_sentences = 3
    if summarization_type == "Extractive":
        num_sentences = st.number_input("Number of sentences for extractive summarization:", min_value=1, value=3)

    if input_text:
        if st.button("Summarize Text"):
            language = detect_language(input_text)
            st.info(f"Detected Language: {language}")
            st.session_state.summary_result = text_summary(input_text, method=summarization_type.lower(), limit=num_sentences if summarization_type == "Extractive" else None)
            
            target_language_input = st.selectbox("Translate input text to", ["en", "es", "fr", "de", "zh-CN", "it", "ja", "ko", "pt", "hi", "ar", "ru", "nl", "sv", "pl", "da"], key='translate_input_text')

            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Input Text:**")
                st.info(input_text)
            with col2:
                st.markdown("**Translated Input Text:**")
                st.info(st.session_state.translated_input)
            with col3:
                st.markdown("**Summarized Text:**")
                st.success(st.session_state.summary_result)

    if st.session_state.summary_result:
        target_language_summary = st.selectbox("Translate summarized text to", ["en", "es", "fr", "de", "zh-CN"], key='translate_summary')
        if st.button("Translate Summary"):
            st.session_state.translated_summary = translate_text(st.session_state.summary_result, target_language_summary)
            col1, col2, col3 = st.columns(3)
            with col3:
                st.markdown("**Translated Summarized Text:**")
                st.success(st.session_state.translated_summary)

elif choice == "Summarize Document":
    colored_header("Summarize Document using txtai", color_name="green-70")
    input_file = st.file_uploader("Upload your document here", type=['pdf'])

    num_sentences = 3  
    if summarization_type == "Extractive":
        num_sentences = st.number_input("Number of sentences for extractive summarization:", min_value=1, value=3)

    if input_file:
        if st.button("Summarize Document"):
            with open("doc_file.pdf", "wb") as f:
                f.write(input_file.getbuffer())
            extracted_text = extract_text_from_pdf("doc_file.pdf")
            language = detect_language(extracted_text)
            st.info(f"Detected Language: {language}")
            st.session_state.summary_result = text_summary(extracted_text, method=summarization_type.lower(), limit=num_sentences if summarization_type == "Extractive" else None)
            
            target_language_input = st.selectbox("Translate extracted text to", ["en", "es", "fr", "de", "zh-CN"], key='translate_doc_input')
            if st.button("Translate Extracted Text"):
                st.session_state.translated_input = translate_text(extracted_text, target_language_input)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Extracted Text:**")
                st.info(extracted_text)
            with col2:
                st.markdown("**Translated Extracted Text:**")
                st.info(st.session_state.translated_input)
            with col3:
                st.markdown("**Summarized Text:**")
                st.success(st.session_state.summary_result)

    if st.session_state.summary_result:
        target_language_summary = st.selectbox("Translate summarized text to", ["en", "es", "fr", "de", "zh-CN"], key='translate_doc_summary')
        if st.button("Translate Summary"):
            st.session_state.translated_summary = translate_text(st.session_state.summary_result, target_language_summary)
            col1, col2, col3 = st.columns(3)
            with col3:
                st.markdown("**Translated Summarized Text:**")
                st.success(st.session_state.translated_summary)