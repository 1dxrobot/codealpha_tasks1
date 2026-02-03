import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/check", methods=["POST"])
def check():
    data = request.get_json() or {}
    url = (data.get("url") or "").strip()
    email_content = (data.get("email_content") or "").strip() or None

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        from detector import detect_phishing
        result = detect_phishing(url, email_content)
        return jsonify({"result": result, "url": url})
    except FileNotFoundError:
        return jsonify({"error": "Model not found. Run: python model_train.py"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
