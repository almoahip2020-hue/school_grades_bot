import subprocess
import sys

print("="*60)
print("🚀 نفق عبد الرحمن السحري لتخطي الحجب وتوصيل الواتساب 🚀")
print("="*60)
print("[*] جاري الاتصال بالسيرفر العالمي عبر منفذ التصفح الآمن (443)...")
print("[!] اضغط Ctrl + C في أي وقت لإيقاف التشغيل.\n")

try:
    # الصيغة الصحيحة: وضع اسم المستخدم المجهول قبل السيرفر
    subprocess.run("ssh -p 443 -R 80:localhost:8000 anonymous@a.pinggy.io", shell=True)
except Exception as e:
    print(f"حدث خطأ أثناء الاتصال: {e}")