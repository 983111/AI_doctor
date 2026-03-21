from PIL import Image
from transformers import pipeline

class MedicalVisionAnalyzer:
    def __init__(self):
        # Note: Using a generic image classification model for demonstration.
        # For a real medical app, you MUST use a specialized medical imaging model.
        print("Loading Vision Model...")
        try:
            self.image_classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
        except Exception as e:
            print(f"Failed to load vision model: {e}")
            self.image_classifier = None

    def analyze_image(self, image_file):
        """Analyzes an uploaded image and returns predicted features."""
        if not self.image_classifier:
            return [{"label": "Model not loaded", "score": 0.0}]
            
        try:
            image = Image.open(image_file).convert('RGB')
            # Get top 3 predictions
            predictions = self.image_classifier(image, top_k=3)
            return predictions
        except Exception as e:
            return [{"label": f"Error processing image: {str(e)}", "score": 0.0}]