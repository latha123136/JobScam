import joblib

# Load model
model = joblib.load("../ml_model/model.pkl")

# Load vectorizer
vectorizer = joblib.load("../ml_model/vectorizer.pkl")

# Example job post
sample_text = """
Earn 1 lakh per month from home.
No interview needed.
Pay registration fee immediately.
"""

# Convert text
text_vector = vectorizer.transform([sample_text])

# Predict
prediction = model.predict(text_vector)

# Output
if prediction[0] == 1:
    print("Fake Job Detected")
else:
    print("Real Job")