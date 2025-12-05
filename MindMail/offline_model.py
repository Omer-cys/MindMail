# offline_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the offline HuggingFace emotion model
model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Map model labels to emojis
label_map = {
    "joy": "Happy 😀",
    "anger": "Angry 😡",
    "sadness": "Sad 😢",
    "fear": "Fear 😨",
    "surprise": "Excited 🤩",
    "love": "Love ❤️",
    "neutral": "Neutral 😐"
}

def model_analyze(text):
    """Analyze emotion using offline HuggingFace model."""
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_id = torch.argmax(logits, dim=1).item()
    label = model.config.id2label[predicted_id].lower()
    return label_map.get(label, "Neutral 😐")
