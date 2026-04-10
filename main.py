import os
from dotenv import load_dotenv
from openai import OpenAI
import cv2  # سيتم استخدامها لاحقاً كما طلبت لمعالجة الفيديو أو الصور

# 1. تحميل المتغيرات البيئية من ملف .env
load_dotenv()

# 2. الحصول على مفتاح API الخاص بمنصة OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# 3. التأكد من أن المفتاح موجود وقابل للاستخدام
if not api_key:
    raise ValueError("الرجاء وضع مفتاح OPENAI_API_KEY الخاص بك داخل ملف .env")

# 4. تهيئة عميل الذكاء الاصطناعي لفتح قناة اتصال مع النماذج
client = OpenAI(api_key=api_key)

print("تم تهيئة النظام الأولي بنجاح! الاتصال بـ OpenAI جاهز.")
