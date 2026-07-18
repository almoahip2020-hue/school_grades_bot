import json
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student

# بيانات الربط المؤقتة مع فيسبوك (سنقوم بتحديثها بمجرد تخطي صفحة التسجيل)
WHATSAPP_TOKEN = "EAAZAEGDzdLLgBR28ZCOmlRkNhlZCMMner8UOZCtuGQhmTccIS7EJqVIUGWrGWHipVsoPgCi8S7erRrRxx1PUAdhpWczH5DZAYkJip3pDm6abnbOPhZBwZCao8SG6yJwWUKdmZBZCwQtKUvfvXijJZCg8WIBhWh2TovBsf19VISQ0kpNR8UyfVdY74lgGqHPNMcGOyZCXwOsEbNA6qUORMzfVLzJjpMmGys56ixU2VjOedI1Fp2CgcnNVfPTfK956ZBPdFQOJaxoLtNRF9ZBckZCKkPYECQRFp3pmdSYyb3fRtZBvAZDZD" # ضع هنا الـ Temporary Access Token لاحقاً
PHONE_NUMBER_ID = "1185832321286393"  # ضع هنا الـ Phone Number ID لاحقاً
VERIFY_TOKEN = "my_secret_token_123" # هذا رمز سري تختاره أنت للربط مع فيسبوك

@csrf_exempt
def whatsapp_webhook(request):
    # 1. خطوة التحقق الأمني الأولية المطلوبة من فيسبوك (GET Request)
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse("خطأ في رمز التحقق الأمني", status=403)

    # 2. خطوة استقبال ومعالجة رسائل الطلاب القادمة من واتساب (POST Request)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # استخراج تفاصيل الرسالة القادمة
            entry = data.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if messages:
                message = messages[0]
                from_number = message.get("from") # رقم هاتف المرسل (ولي الأمر)
                message_text = message.get("text", {}).get("body", "").strip() # النص المرسل (الرقم الأكاديمي)
                
                # البحث عن الطالب باستخدام الرقم الأكاديمي المرسل
                try:
                    student = Student.objects.get(student_id=message_text)
                    
                    # صياغة نص رسالة النتيجة بشكل منسق وجميل باستخدام الـ Bold والإيموجي
                    reply_text = f"*أهلاً بك يا ولي أمر الطالب(ة): {student.name}* 🌟\n\n"
                    reply_text += "📊 *إليك بيان درجات الطالب الفترية:*\n"
                    reply_text += "---------------------------------\n"
                    
                    grades = student.grades.all()
                    if grades:
                        for grade in grades:
                            reply_text += f"📚 *{grade.subject}:* {grade.score} من {grade.max_score}\n"
                    else:
                        reply_text += "⚠️ لم يتم رصد أي درجات لهذا الطالب بعد.\n"
                        
                    reply_text += "---------------------------------\n"
                    reply_text += "نتمنى لأبنائنا دوام التوفيق والنجاح! 🎓"
                    
                except Student.DoesNotExist:
                    # رد في حال لم يتم العثور على الرقم الأكاديمي
                    reply_text = f"❌ عذراً، الرقم الأكاديمي ({message_text}) غير مسجل لدينا في النظام. يرجى التأكد من الرقم وإعادة المحاولة."

                # إرسال الرد التلقائي فوراً إلى واتساب ولي الأمر عبر الـ API الخاص بـ Meta
                send_whatsapp_message(from_number, reply_text)
                
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def send_whatsapp_message(to_number, text_message):
    """دالة مسؤولة عن إرسال الرسائل عبر الـ API لشركة Meta مجاناً"""
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text_message}
    }
    # إرسال الطلب بشكل خلفي غير مرئي
    requests.post(url, headers=headers, json=payload)