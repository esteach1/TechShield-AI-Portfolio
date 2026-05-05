import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 1. إعداد التطبيق وقاعدة البيانات
app = Flask(__name__)
app.config['SECRET_KEY'] = 'zain_cyber_pro_2026'
# ده اسم ملف قاعدة البيانات اللي هيتخزن فيه كل حاجة
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zain_projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 2. تصميم جدول الرسايل في قاعدة البيانات
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100)) # بيعرفنا الرسالة جاية منين
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

# إنشاء قاعدة البيانات فعلياً أول ما نشغل الكود
with app.app_context():
    db.create_all()

# --- 3. المسارات (Routes) ---

# المسار الأساسي (موقعك الشخصي)
@app.route('/')
def home():
    return render_template('index.html')

# مسار المشروع الأول (الـ Landing Page)
@app.route('/project1')
def project1():
    return render_template('landing.html')

# مسار استقبال البيانات وحفظها
@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('message')
    # بنعرف الرسالة جاية من أنهي صفحة (الرئيسية ولا مشروع 1)
    origin = request.referrer 

    if name and email and content:
        # حفظ البيانات في قاعدة البيانات
        new_msg = ContactMessage(
            project_name=origin,
            name=name,
            email=email,
            message=content
        )
        db.session.add(new_msg)
        db.session.commit()
        return f"تم استلام رسالتك يا {name} بنجاح! هرد عليك في أقرب وقت."
    
    return "فيه بيانات ناقصة، ارجع اتأكد تاني!", 400

# مسار "لوحة التحكم" السرية عشان تشوف الرسايل
@app.route('/admin/messages')
def view_messages():
    # بنجيب كل الرسايل من قاعدة البيانات ونرتبها من الأحدث للأقدم
    messages = ContactMessage.query.order_by(ContactMessage.date_sent.desc()).all()
    
    # تنسيق بسيط جداً لعرض الرسايل
    html_content = """
    <body style="background:#111; color:#eee; font-family:sans-serif; padding:20px;">
        <h1 style="color:#3b82f6;">لوحة تحكم رسايل العملاء</h1>
        <hr style="border:0.5px solid #333;">
    """
    
    for msg in messages:
        html_content += f"""
        <div style="background:#222; border-left:5px solid #3b82f6; padding:15px; margin-bottom:15px; border-radius:10px;">
            <p><b>الاسم:</b> {msg.name}</p>
            <p><b>الإيميل:</b> {msg.email}</p>
            <p><b>المصدر:</b> {msg.project_name}</p>
            <p><b>الرسالة:</b> {msg.message}</p>
            <p style="color:#666; font-size:12px;">تاريخ الإرسال: {msg.date_sent.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """
    
    if not messages:
        html_content += "<p>لسه مفيش رسايل وصلت يا هندسة.</p>"
        
    html_content += "</body>"
    return html_content

# تشغيل السيرفر
if __name__ == '__main__':
    app.run(debug=True)