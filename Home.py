import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components
from utils import (
    load_symptoms_df, load_descriptions_df,
    extract_multi_word_symptoms, process_user_input,
    find_disease, get_description
)

st.set_page_config(page_title="Multilingual Symptom Checker", layout="wide")

BASE_DIR = Path(__file__).parent
STATIC = BASE_DIR / "static"
STYLES = BASE_DIR / "styles"

# Load CSS
st.markdown(f"<style>{(STYLES/'base.css').read_text()}</style>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    body {
        background: url('https://static.vecteezy.com/system/resources/thumbnails/042/585/516/small_2x/ai-generated-medical-stethoscope-on-green-background-top-view-with-copy-space-photo.jpg') no-repeat center center fixed;
        background-size: cover;
    }
    .blur-bg {
        backdrop-filter: blur(8px);
        background: rgba(255,255,255,0.3);
        min-height: 100vh;
        width: 100vw;
        position: fixed;
        top: 0;
        left: 0;
        z-index: -1;
    }
    </style>
    <div class="blur-bg"></div>
    """,
    unsafe_allow_html=True
)

# Header
col1, col2, col3 = st.columns([1, 7, 1])
with col1:
    st.image(str(STATIC/"images/icon.png"), width=130)
with col2:
    st.markdown("<h1 style='color:#1976d2; font-size:2.4rem;'>WELCOME TO MULTILINGUAL SYMPTOM CHECKER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#333; text-align: center;'>Get Preliminary Health Guidance based on your Symptoms in your preferred language</p>", unsafe_allow_html=True)
with col3:
    st.image(str(STATIC/"images/medical.jpg"), width=130)

# Load data
@st.cache_data
def load_all():
    s_df = load_symptoms_df()
    d_df = load_descriptions_df()
    multi = extract_multi_word_symptoms(s_df)
    return s_df, d_df, multi

symptoms_df, descriptions_df, multi_word_symptoms = load_all()

# Layout: slideshow left, input form right
left, right = st.columns([2, 2])

with left:
    st.markdown("### Prevention is better than cure")
    import base64
    image_files = [
        "image 1.jpg",
        "image 2.jpg",
        "image 3.jpg",
        "image 4.jpg",
        "Untitled-5.jpg",
        "image 6.jpg"
    ]
    img_tags = ""
    for i, img_name in enumerate(image_files):
        img_path = STATIC / "images" / img_name
        try:
            with open(img_path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            img_tags += f'<img src="data:image/jpeg;base64,{b64}" class="slide{' active' if i==0 else ''}">\n'
        except Exception:
            img_tags += f'<img src="" class="slide{' active' if i==0 else ''}">\n'
    html_slideshow = f"""
    <style>
    .slideshow-container {{
        position: relative;
        width: 100%;
        max-width: 450px;
        height: 400px;
        margin: auto;
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        background: #fff;
    }}
    .slide {{
        display: none;
        width: 95%;
        height: 350px;
        object-fit: contain;
        border-radius: 2px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.12);
    }}
    .slide.active {{
        display: block;
    }}
    </style>
    <div class="slideshow-container">
        {img_tags}
    </div>
    <script>
    var slides = document.querySelectorAll('.slide');
    var current = 0;
    function showSlide(idx) {{
        slides.forEach((img, i) => img.classList.remove('active'));
        slides[idx].classList.add('active');
    }}
    setInterval(function() {{
        current = (current + 1) % slides.length;
        showSlide(current);
    }}, 2000);
    </script>
    """
    components.html(html_slideshow, height=370)

with right:
    st.markdown("### Enter Your Symptoms")
    if "symptom_inputs" not in st.session_state:
        st.session_state.symptom_inputs = [""]
    for i in range(len(st.session_state.symptom_inputs)):
        st.session_state.symptom_inputs[i] = st.text_input(f"Symptom {i+1}", st.session_state.symptom_inputs[i], key=f"symptom_{i}")
    if len(st.session_state.symptom_inputs) < 4:
        if st.button("Add Symptom"):
            st.session_state.symptom_inputs.append("")
    else:
        st.warning("Max 4 symptoms allowed.")
    language = st.selectbox("Select Language", ["en", "te", "ta", "hi"])
    analyze_clicked = st.button("Analyze Symptoms")

# After the two columns, compute and display the result so it appears below both
result_html = ""
if analyze_clicked:
    symptoms = [s for s in st.session_state.symptom_inputs if s.strip()]
    if symptoms:
        processed = process_user_input(" ".join(symptoms), multi_word_symptoms)
        disease = find_disease(processed, symptoms_df)
        if disease:
            desc = get_description(disease, language, descriptions_df)
            if desc:
                result_html = f"""
                <div style=\"width:98vw;max-width:1200px;margin:32px auto 0 auto;padding:32px 24px;background:#eaf6fc;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:left;\">
                    <b style='font-size:1.3rem;'>{disease}</b>:<br><br>{desc}
                </div>
                """
            else:
                result_html = f"<div style='width:98vw;max-width:1200px;margin:32px auto 0 auto;padding:32px 24px;background:#fffbe6;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:center;'><b>Disease found:</b> {disease}, but no description in this language.</div>"
        else:
            result_html = "<div style='width:98vw;max-width:1200px;margin:32px auto 0 auto;padding:32px 24px;background:#ffeaea;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:center;'><b>No matching disease found. Please consult a doctor.</b></div>"
    else:
        result_html = "<div style='width:98vw;max-width:1200px;margin:32px auto 0 auto;padding:32px 24px;background:#fffbe6;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:center;'><b>Please enter at least one symptom.</b></div>"

if result_html:
    st.markdown(result_html, unsafe_allow_html=True)
