# 1. تغيير النسخة إلى 3.11 لضمان عمل المكتبات
FROM python:3.11-slim

WORKDIR /app

# 2. تثبيت أدوات الشبكة الضرورية
RUN apt-get update && apt-get install -y iputils-ping net-tools && rm -rf /var/lib/apt/lists/*

# 3. تثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. نسخ ملفات المشروع
COPY . .

# 5. التوافق مع Flask (مهم جداً للوصول للمتصفح)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

# 6. تشغيل التطبيق مع السماح بالاتصال الخارجي
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
