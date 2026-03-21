from transformers import pipeline

class NLPDiagnosticEngine:
    def __init__(self):
        print("Loading NLP Model...")
        try:
            # Using a lightweight text-generation model for the prototype
            self.chatbot = pipeline("text-generation", model="gpt2")
        except Exception as e:
            print(f"Failed to load NLP model: {e}")
            self.chatbot = None

    def generate_insight(self, patient_text, visual_context=None):
        """Processes patient text and optional visual data to generate insights."""
        if not self.chatbot:
            return "NLP Service is currently unavailable."

        # Construct the prompt
        prompt = f"Patient Symptoms: {patient_text}\n"
        if visual_context:
            prompt += f"Visual Scan Indicators: {visual_context}\n"
        
        prompt += "Preliminary AI Observation (Note: Not a medical diagnosis):\n"

        try:
            response = self.chatbot(prompt, max_length=150, num_return_sequences=1, truncation=True)
            generated_text = response[0]['generated_text']
            
            # Extract just the generated observation part
            observation = generated_text.replace(prompt, "").strip()
            return observation if observation else "Further clinical evaluation is recommended based on these inputs."
        except Exception as e:
            return f"Error generating text: {str(e)}"
