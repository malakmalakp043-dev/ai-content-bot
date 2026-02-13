import os
from groq import Groq
from flask import Flask, request, jsonify

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def home():
    return "AI Content Bot is Running!"

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    prompt = data.get("prompt", "اكتب مقالاً قصيراً عن الذكاء الاصطناعي")
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return jsonify({"content": completion.choices[0].message.content})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
