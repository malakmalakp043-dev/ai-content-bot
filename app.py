import os
from groq import Groq
from flask import Flask, request, jsonify, send_file
from gtts import gTTS

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def home():
    return "Anime Voice Factory is Online!"

@app.route('/make_voice', methods=['POST'])
def make_voice():
    data = request.json
    topic = data.get('topic', 'تريند أنمي')
    
    # توليد السيناريو
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": f"اكتب سيناريو أنمي قصير جداً عن {topic}"}]
    )
    script = completion.choices[0].message.content

    # توليد الصوت
    tts = gTTS(text=script, lang='ar')
    tts.save("voice.mp3")
    
    return send_file("voice.mp3", as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
