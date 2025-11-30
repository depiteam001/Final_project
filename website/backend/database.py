"""
SQLite Database Setup and Models
Lightweight database solution for MentIQ platform
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'mentiq.db')


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def init_db():
    """Initialize database with all tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            user_type TEXT NOT NULL CHECK(user_type IN ('patient', 'doctor')),
            specialty TEXT,
            license_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Consultations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            consultation_date DATE NOT NULL,
            consultation_type TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'cancelled', 'completed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT,
            icon TEXT,
            image_url TEXT,
            link_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL,
            experience_years INTEGER,
            rating REAL DEFAULT 4.5,
            avatar TEXT,
            phone TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'cancelled', 'completed')),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES users(id),
            FOREIGN KEY (doctor_id) REFERENCES users(id)
        )
    ''')
    
    # Chatbot conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatbot_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            risk_prediction REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Assessments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            age INTEGER,
            gender TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            prediction INTEGER,
            prediction_probability REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # Insert initial data
    seed_initial_data()


def seed_initial_data():
    """Seed database with initial articles and doctors"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if articles already exist
    cursor.execute('SELECT COUNT(*) FROM articles')
    if cursor.fetchone()[0] == 0:
        articles = [
            ('Understanding Depression', 'Depression', 
             'Depression is more than sadness. Learn the signs and coping strategies.',
             None, '🧠', None, 'https://www.mayoclinic.org/diseases-conditions/depression/symptoms-causes/syc-20356007'),
            ('Managing Anxiety Disorders', 'Anxiety',
             'Explore proven techniques to manage anxiety and panic attacks.',
             None, '💙', None, 'https://www.medicalnewstoday.com/articles/323454'),
            ('Bipolar Disorder Explained', 'Bipolar',
             'A comprehensive guide to understanding mood episodes and treatment.',
             None, '🌙', None, 'https://en.wikipedia.org/wiki/Bipolar_disorder'),
            ('PTSD Recovery Guide', 'PTSD',
             'Healing from trauma with evidence-based therapeutic approaches.',
             None, '🕊️', None, 'https://neurolaunch.com/ptsd-recovery-stages/'),
            ('OCD Management Tips', 'OCD',
             'Understanding intrusive thoughts and breaking the cycle.',
             None, '✨', None, 'https://www.treatmyocd.com/blog/6-best-strategies-to-combat-obsessive-compulsive-disorder'),
            ('ADHD in Adults', 'ADHD',
             'Recognizing ADHD symptoms and strategies for daily life.',
             None, '⚡', None, 'https://www.healthline.com/health/adhd/adult-adhd')
        ]
        
        cursor.executemany('''
            INSERT INTO articles (title, category, excerpt, content, icon, image_url, link_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', articles)
    
    # Check if doctors already exist
    cursor.execute('SELECT COUNT(*) FROM doctors')
    if cursor.fetchone()[0] == 0:
        doctors = [
            ('Dr. Sarah Ahmed', 'Psychiatrist', 'Egypt', 'Cairo', 12, 4.8, '👩‍⚕️'),
            ('Dr. James Wilson', 'Psychologist', 'USA', 'New York', 10, 4.9, '👨‍⚕️'),
            ('Dr. Fatima Hassan', 'Clinical Psychologist', 'Egypt', 'Alexandria', 8, 4.7, '👩‍⚕️'),
            ('Dr. Ahmed Karim', 'Psychiatrist', 'Egypt', 'Cairo', 15, 4.6, '👨‍⚕️'),
            ('Dr. Emily Brown', 'Psychologist', 'USA', 'New York', 9, 4.8, '👩‍⚕️'),
            ('Dr. Marcus Jones', 'Counselor', 'UK', 'London', 7, 4.7, '👨‍⚕️')
        ]
        
        cursor.executemany('''
            INSERT INTO doctors (name, specialty, country, city, experience_years, rating, avatar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', doctors)
    
    conn.commit()
    conn.close()


# User management functions
def create_user(email, password, name, user_type, specialty=None, license_number=None):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (email, password_hash, name, user_type, specialty, license_number)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, password_hash, name, user_type, specialty, license_number))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        # If doctor, also add to doctors table
        if user_type == 'doctor':
            cursor.execute('''
                INSERT INTO doctors (user_id, name, specialty, country, city, experience_years, rating, avatar)
                VALUES (?, ?, ?, 'Egypt', 'Cairo', 0, 4.5, '👨‍⚕️')
            ''', (user_id, name, specialty or 'General'))
            conn.commit()
        
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def authenticate_user(email, password):
    """Authenticate user and return user data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None


def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return dict(user) if user else None


def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    return dict(user) if user else None

