import os
os.environ["USE_TF"] = "NO"
os.environ["USE_TORCH"] = "YES"
import streamlit as st
from modules.audio_handler import AudioProcessor
from modules.vision_engine import MedicalVisionAnalyzer
from modules.nlp_core import NLPDiagnosticEngine

# --- Initialization ---
# Cache the models so they don't reload on every UI interaction
@st.cache_resource
def load_models():
    vision = MedicalVisionAnalyzer()
    nlp = NLPDiagnosticEngine()
    audio = AudioProcessor()
    return vision, nlp, audio

vision_engine, nlp_engine, audio_handler = load_models()

# --- UI Layout ---
st.set_page_config(page_title="AI Doctor Prototype", layout="wide")
st.title("🩺 AI Doctor: Multimodal Diagnostics Prototype")
st.warning("**DISCLAIMER:** This is an educational prototype. It is not intended for medical use, diagnosis, or treatment.")

# Initialize session state for transcriptions
if "patient_query" not in st.session_state:
    st.session_state.patient_query = ""

# --- Layout Columns ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Input Patient Data")
    
    # Text/Audio Input
    st.subheader("Symptom Description")
    
    if st.button("🎤 Speak Symptoms"):
        with st.spinner("Listening..."):
            transcription = audio_handler.record_and_transcribe()
            st.session_state.patient_query = transcription
            
    text_input = st.text_area("Or type symptoms here:", value=st.session_state.patient_query, height=100)
    
    # Image Input
    st.subheader("Medical Scan / Image")
    uploaded_file = st.file_uploader("Upload an image (X-Ray, Skin, etc.)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Scan", use_column_width=True)

with col2:
    st.header("2. AI Analysis & Insights")
    
    if st.button("Generate Diagnostic Insights", type="primary"):
        if not text_input and not uploaded_file:
            st.error("Please provide either text/audio symptoms or an image scan to begin.")
        else:
            with st.spinner("Processing Multimodal Data..."):
                
                visual_context = None
                # Step A: Process Image if available
                if uploaded_file is not None:
                    st.markdown("### 👁️ Vision Analysis")
                    vision_results = vision_engine.analyze_image(uploaded_file)
                    
                    # Format results for the UI and the NLP model
                    formatted_results = ", ".join([f"{res['label']} ({res['score']:.2f})" for res in vision_results])
                    visual_context = formatted_results
                    st.info(f"Detected Visual Features: {formatted_results}")

                # Step B: Process NLP
                st.markdown("### 🧠 NLP Synthesis")
                if text_input:
                    st.write(f"**Analyzing Symptoms:** {text_input}")
                
                final_insight = nlp_engine.generate_insight(text_input, visual_context)
                
                st.success("**AI Insight:**")
                st.write(final_insight)