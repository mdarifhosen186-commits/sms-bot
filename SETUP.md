# SMS Bot সেটআপ গাইড

## ধাপে ধাপে সেটআপ

### 1️⃣ Telegram Bot টোকেন পান

1. Telegram এ [@BotFather](https://t.me/botfather) খুঁজে পান
2. `/newbot` কমান্ড দিন
3. বটের নাম দিন (যেমন: "My SMS Bot")
4. বটের ইউজারনেম দিন (যেমন: "my_sms_bot")
5. টোকেন কপি করুন এবং সেভ করুন

**উদাহরণ টোকেন:** `1234567890:ABCDEfghIJKLmnopQRSTUVwxyz`

### 2️⃣ Telegram চ্যানেল ও গ্রুপ তৈরি করুন

**চ্যানেল তৈরি করতে:**
1. Telegram এ নতুন চ্যানেল তৈরি করুন
2. চ্যানেলের নাম দিন (যেমন: "My SMS Community")
3. চ্যানেল পাবলিক করুন এবং ইউজারনেম সেট করুন (যেমন: @my_sms_community)
4. বটকে চ্যানেলে অ্যাডমিন হিসেবে যোগ করুন

**গ্রুপ তৈরি করতে:**
1. Telegram এ নতুন গ্রুপ তৈরি করুন
2. গ্রুপের নাম দিন (যেমন: "My SMS Community Chat")
3. গ্রুপ পাবলিক করুন এবং ইউজারনেম সেট করুন (যেমন: @my_sms_community_chat)
4. বটকে গ্রুপে অ্যাডমিন হিসেবে যোগ করুন

**চ্যানেল/গ্রুপ আইডি পেতে:**
1. চ্যানেল/গ্রুপে যান
2. এই বট ফরওয়ার্ড করুন: [@userinfobot](https://t.me/userinfobot)
3. রেসপন্সে চ্যাট আইডি পাবেন (নেগেটিভ নম্বর, যেমন: -1001234567890)

### 3️⃣ Twilio অ্যাকাউন্ট সেটআপ

1. [Twilio.com](https://www.twilio.com) এ যান
2. নতুন অ্যাকাউন্ট তৈরি করুন
3. ভেরিফিকেশন সম্পন্ন করুন
4. Twilio Console এ যান
5. **Account SID** এবং **Auth Token** কপি করুন
6. একটি ফোন নম্বর কিনুন বা ভার্চুয়াল নম্বর সেটআপ করুন

**Twilio ফোন নম্বর ফরম্যাট:** `+1234567890`

### 4️⃣ প্রজেক্ট সেটআপ

```bash
# রেপোজিটরি ক্লোন করুন
git clone https://github.com/mdarifhosen186-commits/sms-bot.git
cd sms-bot

# Python ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন
python -m venv venv

# ভার্চুয়াল এনভায়রনমেন্ট চালু করুন
# Windows এ:
venv\Scripts\activate
# Linux/Mac এ:
source venv/bin/activate

# ডিপেন্ডেন্সি ইনস্টল করুন
pip install -r requirements.txt
```

### 5️⃣ .env ফাইল কনফিগার করুন

```bash
# .env ফাইল তৈরি করুন
cp .env.example .env
```

`.env` ফাইল খুলুন এবং নিচের মান পূরণ করুন:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=আপনার_বট_টোকেন_এখানে

# Telegram Channel & Group
CHANNEL_USERNAME=@আপনার_চ্যানেল_ইউজারনেম
GROUP_USERNAME=@আপনার_গ্রুপ_ইউজারনেম
CHANNEL_ID=-1001234567890
GROUP_ID=-1001234567890

# Twilio Configuration
TWILIO_ACCOUNT_SID=আপনার_অ্যাকাউন্ট_SID
TWILIO_AUTH_TOKEN=আপনার_অথ_টোকেন
TWILIO_PHONE_NUMBER=+1234567890

# Database Configuration
DATABASE_PATH=./sms_bot.db

# Points Configuration
POINTS_PER_REFERRAL=5
POINTS_PER_SMS=1
```

### 6️⃣ বট চালু করুন

```bash
python bot.py
```

আপনি লগে দেখবেন:
```
2026-06-09 12:34:56,789 - root - INFO - Bot started. Press Ctrl+C to stop.
```

### 7️⃣ বট টেস্ট করুন

1. Telegram এ বটের সাথে চ্যাট খুলুন
2. `/start` কমান্ড দিন
3. চ্যানেল ও গ্রুপে যোগ দিন
4. পুনরায় `/start` দিন
5. `/help` দিয়ে সব কমান্ড দেখুন

---

## 🔧 সমস্যা সমাধান

### "Invalid token" এরর

**সমাধান:**
- BotFather থেকে সঠিক টোকেন কপি করুন
- .env ফাইলে পেস্ট করুন
- বটটি পুনরায় চালু করুন

### "Not a member" এরর

**সমাধান:**
1. চ্যানেল ও গ্রুপ আইডি সঠিক আছে কিনা যাচাই করুন
2. বট উভয় জায়গায় অ্যাডমিন আছে কিনা চেক করুন
3. চ্যানেল/গ্রুপ পাবলিক আছে কিনা দেখুন

### Twilio SMS না পাঠানো

**সমাধান:**
1. Twilio ক্রেডেনশিয়াল সঠিক আছে কিনা চেক করুন
2. ফোন নম্বর ফরম্যাট সঠিক আছে কিনা দেখুন (+দিয়ে শুরু)
3. Twilio অ্যাকাউন্টে ক্রেডিট আছে কিনা নিশ্চিত করুন

### ডেটাবেস সংক্রান্ত সমস্যা

**সমাধান:**
```bash
# sms_bot.db ফাইল ডিলিট করুন
rm sms_bot.db
# বট পুনরায় চালু করুন
python bot.py
```

---

## 📱 অ্যাডভান্সড কনফিগারেশন

### পয়েন্ট সিস্টেম কাস্টমাইজ করুন

`.env` ফাইলে এই মান পরিবর্তন করুন:

```env
POINTS_PER_REFERRAL=10    # প্রতি রেফারেল 10 পয়েন্ট
POINTS_PER_SMS=2          # প্রতি SMS 2 পয়েন্ট
```

### উৎপাদন পরিবেশে চালু করুন

Linux সার্ভারে চালু করতে:

```bash
# screen ব্যবহার করে ব্যাকগ্রাউন্ডে চালু করুন
screen -S sms-bot
python bot.py

# Ctrl+A তারপর D দিয়ে ডিটাচ করুন
```

---

## ✅ সফল সেটআপ চেকলিস্ট

- [ ] Telegram Bot Token পেয়েছেন
- [ ] চ্যানেল ও গ্রুপ তৈরি করেছেন
- [ ] বটকে উভয় জায়গায় অ্যাডমিন করেছেন
- [ ] Twilio অ্যাকাউন্ট তৈরি করেছেন
- [ ] .env ফাইল সম্পূর্ণ করেছেন
- [ ] ডিপেন্ডেন্সি ইনস্টল করেছেন
- [ ] বট চালু করেছেন
- [ ] বট সাড়া দেয় টেস্ট করেছেন

সব চেকপয়েন্ট সম্পন্ন? আপনি প্রস্তুত! 🎉
