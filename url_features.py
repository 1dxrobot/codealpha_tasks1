import re
import socket
from urllib.parse import urlparse
from datetime import datetime
import whois

def extract_url_features(url):
    features = {}

    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")
    features["num_at"] = url.count("@")
    features["num_slash"] = url.count("/")
    features["uses_https"] = int(url.startswith("https"))

    parsed = urlparse(url)
    features["has_ip"] = 1 if re.match(r"\d+\.\d+\.\d+\.\d+", parsed.netloc) else 0

    try:
        domain_info = whois.whois(parsed.netloc)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age = (datetime.now() - creation_date).days
        features["domain_age"] = age
    except:
        features["domain_age"] = 0

    return features
