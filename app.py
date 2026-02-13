import os
from groq import Groq
from flask import Flask, request, jsonify, send_file
from gtts import gTTS
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def home():
    return "Anime Factory is Online & Free!"

@app.route('/make_video', methods=['POST'])
def make_video():
    data = request.json
    topic = data.get('topic', 'تريند أنمي جديد')

    # 1. توليد السيناريو عبر Groq
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": f"اكتب سيناريو قصير جداً (30 ثانية) عن {topic} لمقطع تيك توك أنمي."}]
    )
    script = completion.choices[0].message.content

    # 2. تحويل النص إلى صوت (مجاناً عبر gTTS)
    tts = gTTS(text=script, lang='ar')
    audio_path = "voice.mp3"
    tts.save(audio_path)

    # 3. صناعة فيديو بسيط (نص على خلفية ملونة) مجاناً
    # ملاحظة: لصناعة فيديو معقد ستحتاج لرفع صور، لكن هذا للبدء والتأكد من العمل
    bg = ColorClip(size=(720, 1280), color=(30, 30, 30), duration=5)
    txt_clip = TextClip(script[:50], fontsize=50, color='white', size=(600, None), method='caption').set_duration(5)
    video = CompositeVideoClip([bg, txt_clip.set_position('center')])
    
    video_path = "output_anime.mp4"
    video.write_videofile(video_path, fps=24)

    return send_file(video_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
