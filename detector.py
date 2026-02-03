import joblib
import pandas as pd
from urllib.parse import urlparse

from url_features import extract_url_features
from email_analyzer import analyze_email

model = joblib.load("phishing_model.pkl")

# Well-known legitimate domains – never flag these as phishing
TRUSTED_DOMAINS = {
    "google.com", "google.co.in", "google.co.uk",
    "youtube.com", "github.com", "facebook.com", "amazon.com",
    "microsoft.com", "apple.com", "wikipedia.org", "twitter.com",
    "instagram.com", "linkedin.com", "netflix.com", "yahoo.com",
    "cloudflare.com", "stackoverflow.com", "reddit.com",
}

def _get_base_domain(netloc):
    """Get base domain (e.g. www.google.com -> google.com)."""
    parts = netloc.lower().split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])  # last two parts (e.g. google.com)
    return netloc.lower()

def detect_phishing(url, email_content=None):
    parsed = urlparse(url)
    base_domain = _get_base_domain(parsed.netloc or "")
    if base_domain in TRUSTED_DOMAINS:
        return "LEGITIMATE"

    url_features = extract_url_features(url)
    # URLs that use an IP address instead of a domain are highly suspicious (e.g. http://127.0.0.1:8080/login.html)
    if url_features.get("has_ip", 0) == 1:
        return "PHISHING DETECTED"

    df = pd.DataFrame([url_features])
    url_prediction = model.predict(df)[0]

    email_score = 0
    if email_content:
        email_features = analyze_email(email_content)
        email_score = email_features["has_urgent_words"]

    if url_prediction == 1 or email_score == 1:
        return "PHISHING DETECTED"
    else:
        return "LEGITIMATE"

# Example
if __name__ == "__main__":
    test_url = "http://secure-login-update.com"
    test_email = "Urgent! Verify your account immediately."

    result = detect_phishing(test_url, test_email)
    print(result)
