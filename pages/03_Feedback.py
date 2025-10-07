import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
STYLES = BASE_DIR / "styles"
STATIC = BASE_DIR / "static"
st.markdown(f"<style>{(STYLES/'base.css').read_text()}</style>", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 7, 1])
with col1:
    st.image(str(STATIC/"images/icon.png"), width=130)
with col2:
    st.markdown("<h1 style='color:#1976d2; font-size:2.4rem;'>WELCOME TO MULTILINGUAL SYMPTOM CHECKER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#333; text-align: center;'>Get Preliminary Health Guidance based on your Symptoms in your preferred language</p>", unsafe_allow_html=True)
with col3:
    st.image(str(STATIC/"images/medical.jpg"), width=130)


st.markdown("### We value your feedback")
with st.form("feedback-form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    msg = st.text_area("Message")
    submitted = st.form_submit_button("Submit")
if submitted:
    st.success(f"✅ Thank you, {name}, for your feedback!")
