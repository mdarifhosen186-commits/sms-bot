import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

from database import (
    init_database, get_user, create_user, get_user_by_referral_code,
    add_points, deduct_points, get_user_points, create_referral,
    get_referral_count, save_sms_record, set_user_membership,
    is_user_member
)
from utils import (
    generate_referral_code, get_referral_link, extract_referral_code,
    create_welcome_message, create_help_message, create_stats_message,
    create_join_message, get_channel_info, get_group_info
)
from sms_service import send_sms, validate_phone_number

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
GROUP_ID = int(os.getenv('GROUP_ID'))
POINTS_PER_REFERRAL = int(os.getenv('POINTS_PER_REFERRAL', 5))
POINTS_PER_SMS = int(os.getenv('POINTS_PER_SMS', 1))

# Initialize database
init_database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    user_id = user.id
    username = user.username or f"user_{user_id}"
    first_name = user.first_name or username
    
    # Check if user exists
    existing_user = get_user(user_id)
    
    if not existing_user:
        # Get referral code from start parameter
        referral_code = None
        referrer_id = None
        
        if context.args and len(context.args) > 0:
            referral_code_param = context.args[0]
            referral_code_param = extract_referral_code(referral_code_param)
            
            if referral_code_param:
                referrer = get_user_by_referral_code(referral_code_param)
                if referrer:
                    referrer_id = referrer['user_id']
        
        # Generate new referral code for user
        new_referral_code = generate_referral_code()
        
        # Create user
        create_user(user_id, username, first_name, new_referral_code)
        
        # If referred, add points to referrer
        if referrer_id:
            add_points(referrer_id, POINTS_PER_REFERRAL)
            create_referral(referrer_id, user_id)
            
            # Notify referrer
            try:
                context.bot.send_message(
                    chat_id=referrer_id,
                    text=f"🎉 নতুন রেফারেল!\n\n✅ {first_name} আপনার লিংক দিয়ে যোগ দিয়েছে।\n💰 আপনি {POINTS_PER_REFERRAL} পয়েন্ট পেয়েছেন!"
                )
            except:
                pass
    
    # Check if user is member of channel and group
    is_member_channel = await check_member_in_chat(context, user_id, CHANNEL_ID)
    is_member_group = await check_member_in_chat(context, user_id, GROUP_ID)
    
    if not (is_member_channel and is_member_group):
        # User is not member
        await update.message.reply_text(create_join_message())
        return
    
    # User is member
    set_user_membership(user_id, True)
    user = get_user(user_id)
    referral_link = get_referral_link(context.bot.username, user['referral_code'])
    
    welcome_msg = create_welcome_message(first_name, referral_link)
    await update.message.reply_text(welcome_msg)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user_id = update.effective_user.id
    
    if not is_user_member(user_id):
        await update.message.reply_text(create_join_message())
        return
    
    await update.message.reply_text(create_help_message())

async def my_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /my_points command"""
    user_id = update.effective_user.id
    
    if not is_user_member(user_id):
        await update.message.reply_text(create_join_message())
        return
    
    points = get_user_points(user_id)
    message = f"💰 আপনার মোট পয়েন্ট: {points}\n\n1 পয়েন্ট = 1 SMS"
    await update.message.reply_text(message)

async def my_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /my_referral command"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ ব্যবহারকারী খুঁজে পাওয়া যায়নি।")
        return
    
    if not is_user_member(user_id):
        await update.message.reply_text(create_join_message())
        return
    
    referral_link = get_referral_link(context.bot.username, user['referral_code'])
    message = f"""
🔗 আপনার রেফারেল লিংক:

{referral_link}

এই লিংক শেয়ার করুন এবং প্রতিটি নতুন ব্যবহারকারীর জন্য {POINTS_PER_REFERRAL} পয়েন্ট পান!
"""
    await update.message.reply_text(message)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ ব্যবহারকারী খুঁজে পাওয়া যায়নি।")
        return
    
    if not is_user_member(user_id):
        await update.message.reply_text(create_join_message())
        return
    
    referral_count = get_referral_count(user_id)
    stats_msg = create_stats_message(user['username'], user['points'], referral_count)
    await update.message.reply_text(stats_msg)

async def sms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sms command to send SMS"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ ব্যবহারকারী খুঁজে পাওয়া যায়নি।")
        return
    
    if not is_user_member(user_id):
        await update.message.reply_text(create_join_message())
        return
    
    # Parse command
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "❌ সঠিক ফরম্যাট: /sms <নম্বর> <বার্তা>\n\n"
            "উদাহরণ: /sms +8801712345678 হ্যালো, এটি একটি টেস্ট SMS"
        )
        return
    
    phone_number = context.args[0]
    message = ' '.join(context.args[1:])
    
    # Validate phone number
    if not validate_phone_number(phone_number):
        await update.message.reply_text(
            "❌ অবৈধ ফোন নম্বর। নম্বরটি +দিয়ে শুরু হতে হবে।\n"
            "উদাহরণ: +8801712345678"
        )
        return
    
    # Check points
    current_points = get_user_points(user_id)
    if current_points < POINTS_PER_SMS:
        await update.message.reply_text(
            f"❌ পয়েন্ট অপ্রতুষ্ট!\n\n"
            f"আপনার বর্তমান পয়েন্ট: {current_points}\n"
            f"প্রয়োজনীয় পয়েন্ট: {POINTS_PER_SMS}\n\n"
            f"আরও পয়েন্ট পেতে আপনার বন্ধুদের রেফার করুন!"
        )
        return
    
    # Validate message
    if not message or len(message.strip()) == 0:
        await update.message.reply_text("❌ বার্তা খালি হতে পারে না।")
        return
    
    # Send SMS
    success, response = send_sms(phone_number, message)
    
    if success:
        # Deduct points
        deduct_points(user_id, POINTS_PER_SMS)
        
        # Save record
        save_sms_record(user_id, phone_number, message, POINTS_PER_SMS, 'sent')
        
        # Get updated points
        updated_points = get_user_points(user_id)
        
        await update.message.reply_text(
            f"✅ SMS সফলভাবে পাঠানো হয়েছে!\n\n"
            f"📱 নম্বর: {phone_number}\n"
            f"💬 বার্তা: {message[:50]}{'...' if len(message) > 50 else ''}\n"
            f"💰 ব্যবহৃত পয়েন্ট: {POINTS_PER_SMS}\n"
            f"📊 বাকি পয়েন্ট: {updated_points}"
        )
    else:
        save_sms_record(user_id, phone_number, message, 0, 'failed')
        await update.message.reply_text(
            f"❌ SMS পাঠানো ব্যর্থ হয়েছে:\n\n{response}\n\n"
            "অনুগ্রহ করে আবার চেষ্টা করুন।"
        )

async def check_member_in_chat(context, user_id, chat_id):
    """Check if user is member of a chat"""
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except TelegramError:
        return False

def main():
    """Start the bot"""
    # Create application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("my_points", my_points))
    app.add_handler(CommandHandler("my_referral", my_referral))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("sms", sms_command))
    
    # Start polling
    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
