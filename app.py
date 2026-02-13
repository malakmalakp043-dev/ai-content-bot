import os
from groq import Groq
from flask import Flask, request, jsonify

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# تخصص القناة: قصص ونظريات الأنمي
CHANNEL_NICHE = "Anime Stories and Trends"

@app.route('/')
def home():
    return "Anime AI Engine is Running!"

@app.route('/generate_anime_video', methods=['POST'])
def generate_anime_content():
    # البوت سيبحث عن تريند في هذا المجال أو يحلل فكرتك
    data = request.json
    user_topic = data.get('topic', 'أحدث تريند في عالم الأنمي حالياً')

    prompt = f"""
    أنت خبير في محتوى الأنمي والتريندات. 
    المجال: {CHANNEL_NICHE}
    الموضوع المطلوب: {user_topic}
    
    قم بالآتي:
    1. ابحث عن فكرة "تريند" (Viral) تتعلق بهذا الموضوع.
    2. اكتب سيناريو فيديو قصير (Script) مشوق جداً.
    3. قسم السيناريو إلى (مشاهد) مع وصف لكل مشهد ليتم استخدامه في MovieFlow.
    4. اجعل اللغة العربية بسيطة وجذابة لمحبي الأنمي.
    """

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({
        "status": "success",
        "content": completion.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
