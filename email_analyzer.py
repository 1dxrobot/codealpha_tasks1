import re

PHISHING_KEYWORDS = [
    "urgent", "verify", "account suspended",
    "login immediately", "click below",
    "password", "security alert"
]

def analyze_email(content):
    features = {}

    content_lower = content.lower()

    features["has_urgent_words"] = int(any(word in content_lower for word in PHISHING_KEYWORDS))
    features["num_links"] = len(re.findall(r"http[s]?://", content))
    features["has_html"] = int("<html>" in content_lower)
    features["content_length"] = len(content)

    return features
    