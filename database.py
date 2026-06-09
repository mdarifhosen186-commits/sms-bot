import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.getenv('DATABASE_PATH', './sms_bot.db')

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            points INTEGER DEFAULT 0,
            referral_code TEXT UNIQUE,
            referred_by INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_member BOOLEAN DEFAULT 0
        )
    ''')
    
    # Referrals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER,
            referred_user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(user_id),
            FOREIGN KEY (referred_user_id) REFERENCES users(user_id)
        )
    ''')
    
    # SMS History table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sms_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            recipient_number TEXT,
            message TEXT,
            points_used INTEGER,
            status TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user(user_id):
    """Get user information"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def create_user(user_id, username, first_name, referral_code):
    """Create a new user"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (user_id, username, first_name, referral_code)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, referral_code))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_referral_code(referral_code):
    """Get user by referral code"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE referral_code = ?', (referral_code,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def add_points(user_id, points):
    """Add points to user"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET points = points + ? WHERE user_id = ?', (points, user_id))
    conn.commit()
    conn.close()

def deduct_points(user_id, points):
    """Deduct points from user"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET points = points - ? WHERE user_id = ?', (points, user_id))
    conn.commit()
    conn.close()

def get_user_points(user_id):
    """Get user's current points"""
    user = get_user(user_id)
    return user['points'] if user else 0

def create_referral(referrer_id, referred_user_id):
    """Create a referral record"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO referrals (referrer_id, referred_user_id)
            VALUES (?, ?)
        ''', (referrer_id, referred_user_id))
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def get_referral_count(user_id):
    """Get total referrals for a user"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM referrals WHERE referrer_id = ?', (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def save_sms_record(user_id, recipient_number, message, points_used, status='sent'):
    """Save SMS record to history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sms_history (user_id, recipient_number, message, points_used, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, recipient_number, message, points_used, status))
    conn.commit()
    conn.close()

def set_user_membership(user_id, is_member):
    """Update user membership status"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_member = ? WHERE user_id = ?', (is_member, user_id))
    conn.commit()
    conn.close()

def is_user_member(user_id):
    """Check if user is a member of channel and group"""
    user = get_user(user_id)
    return user['is_member'] if user else False
