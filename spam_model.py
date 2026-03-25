from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Sample training data
texts = [
    "win money now",
    "free prize click link",
    "urgent account update",
    "hello i need help",
    "please contact me",
    "i want to know about your services"
]

labels = [1,1,1,0,0,0]  # 1 = spam, 0 = normal

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X,labels)

# save model
joblib.dump(model,"spam_model.pkl")
joblib.dump(vectorizer,"vectorizer.pkl")

print("Model created successfully")