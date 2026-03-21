from transformers import pipeline

class NLPDiagnosticEngine:
    def __init__(self):
        print("Loading NLP Model...")
        try:
            # Swapped gpt2 for an instruction-tuned model
            self.chatbot = pipeline("text2text-generation", model="google/flan-t5-base")
        except Exception as e:
            print(f"Failed to load NLP model: {e}")
            self.chatbot = None

    def generate_insight(self, patient_text, visual_context=None):
        """Processes patient text and optional visual data to generate insights."""
        if not self.chatbot:
            return "NLP Service is currently unavailable."

        # Construct a direct instruction prompt for the model
        prompt = f"As an AI medical assistant, provide a short, preliminary observation based on these patient symptoms: '{patient_text}'."
        if visual_context:
            prompt += f" Additionally, consider these visual scan features: '{visual_context}'."

        try:
            # Generate the response
            response = self.chatbot(prompt, max_length=150, truncation=True)
            generated_text = response[0]['generated_text']
            
            return generated_text if generated_text else "Further clinical evaluation is recommended based on these inputs."
        except Exception as e:
            return f"Error generating text: {str(e)}"
