
#code
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# 1. Load dataset
df = pd.read_csv("documents.csv")

X = df['text']
y = df['label']

# 2. Build pipeline: TF-IDF + Classifier
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LogisticRegression(max_iter=1000))
])

# 3. Train the model
model_pipeline.fit(X, y)

# 4. Save the trained model
joblib.dump(model_pipeline, "model/document_classifier.pkl")

print("✅ Model trained and saved as model/document_classifier.pkl")


# usage
import joblib

# Load the saved model
model_pipeline = joblib.load("model/document_classifier.pkl")

def predict_document(text):
    predicted_label = model_pipeline.predict([text])[0]
    return predicted_label

# Example usage:
if __name__ == "__main__":
    new_docs = [
        "This is a receipt for your last electricity bill payment.",
        "The Prime Minister addressed the nation about climate change.",
        "Here is my CV for the software developer position."
    ]

    for doc in new_docs:
        print(f"Document: {doc}")
        print(f"Predicted Type: {predict_document(doc)}\n")

#install
# Install dependencies
pip install pandas scikit-learn joblib

# Train the model
python train_classifier.py

# Predict with new documents
python predict_document.py

