import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

from url_features import extract_url_features

data = pd.read_csv("dataset/phishing.csv")

feature_rows = []
labels = []

for index, row in data.iterrows():
    features = extract_url_features(row["url"])
    feature_rows.append(features)
    labels.append(row["label"])

X = pd.DataFrame(feature_rows)
y = labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

joblib.dump(model, "phishing_model.pkl")
