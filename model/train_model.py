import pandas as pd
import re
import nltk
import joblib
import os

from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Download stopwords (only first time)
nltk.download("stopwords")

# =========================
# LOAD DATASET (SAFE PATH)
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "complaints.csv")

df = pd.read_csv(DATA_PATH)

# Remove empty rows (important)
df = df.dropna(subset=["text"])

# =========================
# TEXT CLEANING
# =========================
stop_words = set(stopwords.words("english"))

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = [w for w in text.split() if w not in stop_words]
    return " ".join(words)

df["clean_text"] = df["text"].apply(clean_text)

# =========================
# TRAIN / TEST SPLIT
# =========================
X = df["clean_text"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# ML PIPELINE
# =========================
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

# =========================
# TRAIN MODEL
# =========================
model.fit(X_train, y_train)

# =========================
# EVALUATION
# =========================
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, os.path.join(os.path.dirname(__file__), "complaint_model.pkl"))
print("Model saved successfully")
