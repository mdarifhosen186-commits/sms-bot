import random
import string
import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')
GROUP_USERNAME = os.getenv('GROUP_USERNAME')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
GROUP_ID = int(os.getenv('GROUP_ID'))

def generate_referral_code():
    """Generate a unique referral code"""
    return 'ref_' + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def get_referral_link(bot_username, referral_code):
    """Generate referral link for user"""
    return f"https://t.me/{bot_username}?start={referral_code}"

def get_channel_info():
    """Get channel information"""
    return {
        'username': CHANNEL_USERNAME,
        'id': CHANNEL_ID
    }

def get_group_info():
    """Get group information"""
    return {
        'username': GROUP_USERNAME,
        'id': GROUP_ID
    }

def format_message(text):
    """Format message text"""
    return text.strip()

def extract_referral_code(start_param):
    """Extract referral code from start parameter"""
    if start_param and start_param.startswith('ref_'):
        return start_param
    return None

def create_welcome_message(username, referral_link):
    """Create welcome message for user"""
    message = f"""
🎉 স্বাগতম {username}!

আমি একটি এসএমএস বট যা আপনাকে সম্পূর্ণ গোপনীয়তার সাথে SMS পাঠাতে সাহায্য করব।

📋 এখন কী করবেন:

1️⃣ আমাদের চ্যানেল ও গ্রুপে যোগ দিন (বাধ্যতামূলক)
2️⃣ আপনার রেফারেল লিংক শেয়ার করুন ও পয়েন্ট অর্জন করুন
3️⃣ পয়েন্ট ব্যবহার করে SMS পাঠান

💡 রেফারেল লিংক:
{referral_link}

প্রতি রেফারেল = ৫ পয়েন্ট
প্রতি SMS = ১ পয়েন্ট

আরও সাহায্যের জন্য /help কমান্ড ব্যবহার করুন।
"""
    return message.strip()

def create_help_message():
    """Create help message"""
    message = """
📚 উপলব্ধ কমান্ড:

/start - বট শুরু করুন
/help - সাহায্য পান
/my_points - আপনার পয়েন্ট দেখুন
/my_referral - আপনার রেফারেল লিংক দেখুন
/stats - আপনার পরিসংখ্যান দেখুন

📨 SMS পাঠানোর উপায়:
/sms <নম্বর> <বার্তা>

উদাহরণ:
/sms +8801712345678 হ্যালো, এটি একটি টেস্ট SMS

⚠️ গুরুত্বপূর্ণ:
- SMS পাঠাতে আপনার পয়েন্ট থাকতে হবে
- প্রতিটি SMS এর জন্য ১ পয়েন্ট খরচ হয়
- পয়েন্ট বাড়াতে আরও মানুষকে রেফার করুন
"""
    return message.strip()

def create_stats_message(username, points, referral_count):
    """Create statistics message"""
    message = f"""
📊 আপনার পরিসংখ্যান:

👤 ব্যবহারকারী: {username}
💰 মোট পয়েন্ট: {points}
🔗 রেফারেল: {referral_count}
💸 আয়: {referral_count * 5} পয়েন্ট (রেফারেল থেকে)

💡 টিপস:
- আপনার রেফারেল লিংক শেয়ার করে আরও পয়েন্ট অর্জন করুন
- প্রতিটি সফল রেফারেল = ৫ পয়েন্ট
"""
    return message.strip()

def create_join_message():
    """Create message prompting user to join channel and group"""
    channel_info = get_channel_info()
    group_info = get_group_info()
    
    message = f"""
🔒 অ্যাক্সেস সীমাবদ্ধ

এই বটটি ব্যবহার করতে আপনাকে নীচের দুটিতে যোগ দিতে হবে:

1️⃣ চ্যানেল: {channel_info['username']}
2️⃣ গ্রুপ: {group_info['username']}

উভয়েই যোগ দিলে, /start আবার চেষ্টা করুন এবং আপনার রেফারেল লিংক পাবেন।
"""
    return message.strip()
