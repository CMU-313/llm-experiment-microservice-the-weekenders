import os
from flask import Flask, request, jsonify
from src.translator import translate_content

app = Flask(__name__)

@app.get("/health")
def health():
    return "ok", 200

@app.post("/translate")
def translator():
    data = request.get_json(silent=True) or {}
    content = data.get("content", "")
    is_english, translated_content = translate_content(content)
    return jsonify({
        "is_english": is_english,
        "translated_content": translated_content,
    })

@app.get("/")
def root():
    return "translator up", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
