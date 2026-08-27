# AlFalah Backend API

هذا هو الـ Backend المستقل لتطبيق الفلاح. تم بناؤه باستخدام Node.js و TypeScript و Express.

## المتطلبات الأساسية
- Node.js (v18+)
- ملف Service Account الخاص بـ Firebase.

## التثبيت

1. ادخل إلى المجلد:
```bash
cd backend
```

2. ثبت الاعتمادات (Dependencies):
```bash
npm install
```

3. قم بإعداد متغيرات البيئة:
- انسخ ملف `.env.example` وقم بتسميته `.env`.
- ضع المسار الصحيح لملف `serviceAccountKey.json` الخاص بـ Firebase.

## التشغيل

لتشغيل السيرفر في وضع التطوير (Development):
```bash
npm run dev
```

لعمل Build وتشغيله في الإنتاج (Production):
```bash
npm run build
npm start
```

## الـ Endpoints الموجودة حالياً

- `GET /health` : للتحقق من أن السيرفر يعمل.
- `POST /api/ai/chat` : مسار المحادثة مع المساعد الزراعي (محمي بالمصادقة).

## المصادقة (Authentication)
التطبيق يعتمد على Firebase Authentication. الـ Backend لا يحفظ كلمات المرور بل يتحقق من `ID Token` المرسل في الـ Header للطلبات:
`Authorization: Bearer <FIREBASE_ID_TOKEN>`

## ملاحظات المرحلة الحالية
في هذه المرحلة، خدمة Gemini غير مفعلة، ولذلك سيعيد الـ API رسالة توضح أن الخدمة غير مفعلة حالياً دون استخدام أي بيانات وهمية.
