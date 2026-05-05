import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# إعداد التطبيق الخاص بمشروع الذكاء الاصطناعي
app = Flask(__name__)
app.secret_key = 'zain_ai_exclusive_2026'

# قاعدة بيانات جديدة خاصة بالمشروع ده بس
# الملف ده هيظهر في فولدر المشروع باسم ai_hub_data.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_hub_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# موديل تخزين رسايل الزوار المهتمين بالذكاء الاصطناعي
class AIContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_name = db.Column(db.String(100))
    visitor_email = db.Column(db.String(120))
    inquiry_type = db.Column(db.String(50)) # نوع الاستفسار (بحث، برمجة، ملفات)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# إنشاء قاعدة البيانات المستقلة
with app.app_context():
    db.create_all()

# --- المسارات (Routes) ---

@app.route('/')
def index():
    # هيفتح ملف ai_hub.html اللي إحنا عملناه
    return render_template('ai_hub.html')

@app.route('/submit_inquiry', methods=['POST'])
def submit_inquiry():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('message')
    
    if name and email and content:
        new_entry = AIContact(
            visitor_name=name,
            visitor_email=email,
            message=content
        )
        db.session.add(new_entry)
        db.session.commit()
        return f"شكراً يا {name}.. تم استلام اهتمامك بمجال الـ AI بنجاح!"
    
    return "برجاء التأكد من إدخال البيانات كاملة.", 400

# لوحة تحكم بسيطة وسريعة للمشروع ده بس عشان تشوف مين مهتم بالـ AI
@app.route('/view-leads')
def view_leads():
    leads = AIContact.query.order_by(AIContact.timestamp.desc()).all()
    output = "<body style='background:#020617; color:white; font-family:sans-serif; padding:20px;'>"
    output += "<h1 style='color:#3b82f6;'>قائمة المهتمين بمشروع AI Hub</h1><hr border='0.1'>"
    for lead in leads:
        output += f"""
        <div style='border:1px solid #1e293b; padding:15px; margin:10px 0; border-radius:10px; background:#0f172a;'>
            <p><b>الاسم:</b> {lead.visitor_name}</p>
            <p><b>الإيميل:</b> {lead.visitor_email}</p>
            <p><b>الرسالة:</b> {lead.message}</p>
            <p><small style='color:#64748b;'>التوقيت: {lead.timestamp}</small></p>
        </div>
        """
    if not leads: output += "<p>لا يوجد مهتمين حتى الآن.</p>"
    return output

if __name__ == '__main__':
    # تشغيل السيرفر المستقل
    app.run(debug=True, port=5005) # بورت مختلف عشان ميتعارضش مع أي مشروع تاني شغال