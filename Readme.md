# AI Doctor Prototype

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Architecture & Components](#architecture--components)
4. [Installation & Setup](#installation--setup)
5. [Running the Application](#running-the-application)
6. [Configuration & Environment Variables](#configuration--environment-variables)
7. [User Interface Walkthrough](#user-interface-walkthrough)
8. [Extending & Customizing the Prototype](#extending--customizing-the-prototype)
9. [Testing & Debugging](#testing--debugging)
10. [Contributing](#contributing)
11. [License](#license)
12. [Disclaimer](#disclaimer)

---

## Overview
**AI Doctor** is a multimodal diagnostic prototype that combines **speech-to-text**, **computer vision**, and **natural language processing** (NLP) to generate AI-driven insights from patient-provided data. It is built using **Streamlit** for rapid UI development and leverages PyTorch for deep learning models.

The goal of this project is **educational**—to demonstrate how various AI modalities can be integrated into a simple web-based diagnostic assistant. It is **not** intended for real medical diagnosis, treatment, or decision-making.

---

## Features
- **Voice Input**: Patients can speak symptoms, which are transcribed using an `AudioProcessor`.
- **Text Input**: Traditional free-text symptom entry.
- **Image Upload**: Upload medical scans (X‑Ray, skin lesions, etc.) for visual analysis.
- **Multimodal Fusion**: Combines visual context (detected objects/labels) with textual symptoms to produce a synthesized diagnostic insight.
- **Caching**: Streamlit’s `@st.cache_resource` ensures heavy model loads happen only once per session.
- **Responsive Layout**: Two-column layout with intuitive UI sections.
- **Extensible Architecture**: Modular code separation (`audio_handler`, `vision_engine`, `nlp_core`) for easy swapping of underlying models or services.

---

## Architecture & Components
### 1. `app.py`
- Entry point for the Streamlit web app.
- Handles UI layout, session state, and orchestrates model calls.
- Sets environment flags to control backend model selection (`USE_TF`, `USE_TORCH`).

### 2. `modules/audio_handler.py`
- Provides `AudioProcessor` class.
- Implements `record_and_transcribe()` to capture audio and convert to text using speech recognition utilities (e.g., `speech_recognition` & `pyaudio` or `whisper`).

### 3. `modules/vision_engine.py`
- Provides `MedicalVisionAnalyzer` class.
- Implements `analyze_image()` to process medical images with a pre‑trained PyTorch model (e.g., a custom ResNet or TorchVision model).
- Returns a list of dictionaries containing `label` and `score` for each detected feature.

### 4. `modules/nlp_core.py`
- Provides `NLPDiagnosticEngine` class.
- Implements `generate_insight(text, visual_context)` to synthesize a diagnostic narrative from textual symptoms and optional visual context.

### 5. Dependency Files
- `requirements.txt`: Python package dependencies.
- `packages.txt`: Additional system-level packages (if any) required for audio/video processing.

---

## Installation & Setup

### Prerequisites
- **Python**: >= 3.9
- **pip**: latest version
- **Git**: optional, for cloning the repository

### Step‑by‑Step Installation

# 1. Clone the repository (if not already done)
git clone https://github.com/yourusername/AI_doctor.git
cd AI_doctor

# 2. Create a virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install any additional system packages (if specified)
# Example for Ubuntu/Debian:
# sudo apt-get install -y ffmpeg libasound2 lib PortAudio
# Refer to packages.txt for exact commands
### Optional: Set Environment Variables
The app automatically sets the following flags to control which backend model is used:

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_TF` | `NO` | Disable TensorFlow models (currently unused). |
| `USE_TORCH` | `YES` | Enable PyTorch models for vision processing. |

If you need to override defaults, export them before launching:

export USE_TF="YES"
export USE_TORCH="NO"

---

## Running the Application

# Ensure virtual environment is active (see above)
python app.py

- The Streamlit server will start on `http://localhost:8501`.
- Use the UI to input symptoms (voice or text) and optionally upload an image.
- Click **Generate Diagnostic Insights** to see the multimodal AI output.

### Production Deployment (Optional)
For deploying to a cloud platform (e.g., Streamlit Cloud, Heroku, AWS Elastic Beanstalk), ensure the following:
- `requirements.txt` lists all Python dependencies.
- `streamlit` config is set to `offline` if needed.
- Large model files are included in the repo or mounted via a cloud storage bucket.

---

## Configuration & Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `USE_TF` | String | `"NO"` | Controls loading of TensorFlow models. Set to `"YES"` if you implement TF‑based components. |
| `USE_TORCH` | String | `"YES"` | Controls loading of PyTorch models for vision. Set to `"NO"` to skip vision processing (useful for testing NLP only). |

These variables are defined at the top of `app.py` and can be overridden in the shell before running `app.py`.

---

## User Interface Walkthrough

### 1. Layout Overview
The UI is split into two columns using `st.columns(2)`:
- **Left Column**: Input area (symptom description via voice or text, image upload).
- **Right Column**: Analysis area (vision results, NLP synthesis, final AI insight).

### 2. Input Section
- **Symptom Description**
  - *Voice*: Click the “🎤 Speak Symptoms” button → microphone activation → transcription appears in the text box.
  - *Text*: Directly type symptoms in the provided textarea.
- **Medical Scan / Image**
  - Drag‑and‑drop or browse to upload a medical image file (`jpg`, `jpeg`, `png`).
  - Uploaded images are displayed inline for verification.

### 3. Analysis Section
- **Generate Diagnostic Insights** (Primary button)
  - Triggers multimodal pipeline.
  - If no input is provided, an error is shown.
- **Vision Analysis** (if image uploaded)
  - Shows detected visual features with confidence scores.
  - Results are passed to the NLP engine as context.
- **NLP Synthesis**
  - Displays the text being analyzed (symptoms) and runs the insight generation.
- **AI Insight**
  - Final output is presented under a success banner.

### 4. Session State
- `st.session_state.patient_query` stores the last transcribed or typed symptom description to preserve user input across page refreshes.

---

## Extending & Customizing the Prototype

### Adding New Audio Backends
1. Edit `modules/audio_handler.py`.
2. Implement a new class or extend `AudioProcessor` with alternative APIs (`speech_recognition`, `Whisper`, `DeepSpeech`).
3. Update `app.py` import if you rename the class.

### Swapping Vision Models
1. Replace the model loading logic inside `MedicalVisionAnalyzer.__init__` (or add a factory method).
2. Adjust `analyze_image` output format to match expected list of `{label, score}` dicts.
3. Update `requirements.txt` if you add a new library (e.g., `torchvision`, `opencv-python`).

### Enhancing NLP Engine
1. Modify `NLPDiagnosticEngine.generate_insight` to incorporate more sophisticated language models (e.g., HuggingFace Transformers).
2. Provide additional context (e.g., patient age, gender) via new session state variables.
3. Ensure the method returns a string suitable for UI rendering.

### UI Customizations
- Add more columns or tabs using Streamlit’s `st.tabs`, `st.expander`, or `st.sidebar`.
- Implement validation messages for audio recording errors.
- Style with `st.markdown`, `st.caption`, or custom CSS via `st.markdown("<style>...</style>", unsafe_allow_html=True)`.

### Integrating Backend APIs
- Extend the app to call external medical APIs (e.g., for drug interactions) by adding new modules and exposing them via a button in the UI.

---

## Testing & Debugging

### Unit Tests
The repository does not currently contain a `tests/` folder, but you can add tests using `pytest`:

pip install pytest
# Create tests/test_vision_engine.py, test_nlp_core.py, test_audio_handler.py
pytest

### Common Debugging Tips
- **Audio Issues**: Verify microphone permissions, install `pyaudio` or `sounddevice`, and ensure `ffmpeg` is available.
- **Vision Model Errors**: Check that the model weights are correctly downloaded and that `torch` version matches the model’s requirements.
- **NLP Failures**: Ensure the input text is non‑empty; handle `None` for visual context gracefully.

### Logging
Add `import logging` at the top of each module and configure a logger:

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

Use `logger.info`, `logger.error` for debugging.

---

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository and create a new branch for your feature/bug fix.
2. Write **clear, well‑documented code** that aligns with existing style (PEP‑8, type hints where possible).
3. Add **unit tests** for any new functionality.
4. Update the **README** to reflect new features or usage changes.
5. Submit a **Pull Request** with a concise description of your changes.

### Code Style
- Use 4‑space indentation.
- Limit line length to 88 characters (as per `black` defaults).
- Include docstrings for public functions and classes.
- Type hint arguments and return values where feasible.

### License
See `LICENSE` file for details. By default, this project is released under the MIT License.

---

## License
MIT License

Copyright (c) 2024 <Your Name>

Permission is hereby granted, free of charge, to any person obtaining a copy...

---

## Disclaimer
**⚠️ This application is strictly an educational prototype.**  
It does **not** replace professional medical advice, diagnosis, or treatment.  
Use it only for demonstration and research purposes.  
The developers and contributors are not liable for any misuse or reliance on the AI-generated insights.

--- 

*End of README*