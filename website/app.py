"""
Flask API for MentIQ Mental Health Platform
Serves the frontend website and provides API endpoints with database integration
"""

from flask import Flask, send_from_directory, jsonify, request, session
from flask_cors import CORS
import os
import sys
import joblib
import pandas as pd
import numpy as np
from functools import wraps
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from database import (
    init_db, get_db_connection, create_user, authenticate_user,
    get_user_by_id, get_user_by_email
)

# Initialize Flask app
app = Flask(__name__, 
            template_folder='frontend',
            static_folder='frontend',
            static_url_path='')

# Enable CORS for API endpoints - allow all origins in development
# In production, restrict to specific origins
CORS(app, 
     supports_credentials=True,
     resources={r"/api/*": {"origins": "*"}},  # Allow all origins for API endpoints
     allow_headers=['Content-Type'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
MODEL_DIR = os.path.join(os.path.dirname(BASE_DIR), 'saved_models')

# Load ML model for chatbot
ML_PIPELINE = None
try:
    model_path = os.path.join(MODEL_DIR, 'full_pipeline.pkl')
    if os.path.exists(model_path):
        ML_PIPELINE = joblib.load(model_path)
        print("✅ ML model loaded successfully")
    else:
        print("⚠️ ML model not found, using fallback responses")
except Exception as e:
    print(f"⚠️ Error loading ML model: {e}. Using fallback responses.")


# ==================== Authentication Decorator ====================

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


# ==================== Frontend Routes ====================

@app.route('/')
def index():
    """Serve the main index page"""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/login')
def login_page():
    """Serve the login page"""
    return send_from_directory(FRONTEND_DIR, 'login.html')


@app.route('/assessment')
def assessment():
    """Serve the assessment page"""
    return send_from_directory(FRONTEND_DIR, 'assessment.html')


@app.route('/doctor-dashboard')
def doctor_dashboard():
    """Serve the doctor dashboard page"""
    return send_from_directory(FRONTEND_DIR, 'doctor-dashboard.html')


@app.route('/profile')
def profile():
    """Serve the profile page"""
    return send_from_directory(FRONTEND_DIR, 'profile.html')


# ==================== Static Files ====================

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, images, etc.)"""
    return send_from_directory(FRONTEND_DIR, filename)


# ==================== Authentication API Routes ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        required_fields = ['email', 'password', 'name', 'user_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        email = data['email']
        password = data['password']
        name = data['name']
        user_type = data['user_type']
        specialty = data.get('specialty')
        license_number = data.get('license_number')
        
        # Check if user already exists
        if get_user_by_email(email):
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 400
        
        # Create user
        user_id = create_user(email, password, name, user_type, specialty, license_number)
        
        if user_id:
            # Set session
            session['user_id'] = user_id
            session['user_type'] = user_type
            
            user = get_user_by_id(user_id)
            return jsonify({
                'success': True,
                'message': 'Registration successful',
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'user_type': user['user_type']
                }
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create user'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user - user type is determined from database, not from request"""
    try:
        data = request.get_json()
        
        if 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Email and password required'
            }), 400
        
        user = authenticate_user(data['email'], data['password'])
        
        if user:
            # Verify user type is valid (must be 'patient' or 'doctor')
            if user['user_type'] not in ['patient', 'doctor']:
                return jsonify({
                    'success': False,
                    'error': 'Invalid user account type'
                }), 403
            
            # Update last login
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET last_login = ? WHERE id = ?',
                (datetime.now().isoformat(), user['id'])
            )
            conn.commit()
            conn.close()
            
            # Set session
            session['user_id'] = user['id']
            session['user_type'] = user['user_type']
            
            user_response = {
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
                'user_type': user['user_type']  # User type from database
            }
            
            # Also include 'type' for backward compatibility
            user_response['type'] = user['user_type']
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user_response
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200


@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current authenticated user"""
    user_id = session.get('user_id')
    user = get_user_by_id(user_id)
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
                'user_type': user['user_type']
            }
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404


@app.route('/api/profile/assessment', methods=['GET'])
@login_required
def get_user_assessment():
    """Get user's latest assessment"""
    try:
        user_id = session.get('user_id')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM assessments 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        ''', (user_id,))
        
        assessment = cursor.fetchone()
        conn.close()
        
        if assessment:
            return jsonify({
                'success': True,
                'assessment': dict(assessment)
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No assessment found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profile/appointments', methods=['GET'])
@login_required
def get_user_appointments():
    """Get user's appointments"""
    try:
        user_id = session.get('user_id')
        user_type = session.get('user_type')
        
        print(f"Getting appointments for user_id: {user_id}, user_type: {user_type}")  # Debug log
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if user_type == 'doctor':
            # For doctors, get appointments where they are the doctor
            # doctor_id in appointments table references users.id
            cursor.execute('''
                SELECT a.*, u.name as patient_name, u.email as patient_email
                FROM appointments a
                JOIN users u ON a.patient_id = u.id
                WHERE a.doctor_id = ?
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            ''', (user_id,))
            print(f"Querying appointments for doctor_id: {user_id}")  # Debug log
        else:
            # For patients, show all appointments (pending can be canceled, confirmed cannot)
            # Join with doctors table using user_id, and also get doctor user info
            cursor.execute('''
                SELECT a.*, 
                       d.name as doctor_name, 
                       d.specialty, 
                       d.city, 
                       d.country,
                       u.name as doctor_user_name
                FROM appointments a
                LEFT JOIN doctors d ON a.doctor_id = d.user_id
                LEFT JOIN users u ON a.doctor_id = u.id
                WHERE a.patient_id = ?
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            ''', (user_id,))
            print(f"Querying appointments for patient_id: {user_id}")  # Debug log
        
        appointments = cursor.fetchall()
        print(f"Found {len(appointments)} appointments")  # Debug log
        
        # Debug: print all appointments
        for apt in appointments:
            print(f"Appointment: {dict(apt)}")  # Debug log
        
        conn.close()
        
        appointments_list = []
        for apt in appointments:
            apt_dict = dict(apt)
            # Format the appointment data
            if user_type == 'doctor':
                apt_dict['patient'] = apt_dict.get('patient_name', 'Unknown Patient')
                apt_dict['patient_email'] = apt_dict.get('patient_email', '')
            else:
                # Use doctor_name from doctors table, fallback to doctor_user_name from users table
                apt_dict['doctor'] = apt_dict.get('doctor_name') or apt_dict.get('doctor_user_name', 'Unknown Doctor')
                apt_dict['location'] = f"{apt_dict.get('city', '')}, {apt_dict.get('country', '')}".strip()
                if not apt_dict['location'] or apt_dict['location'] == ', ':
                    apt_dict['location'] = 'Location TBD'
            
            appointments_list.append(apt_dict)
        
        print(f"Returning {len(appointments_list)} appointments")  # Debug log
        return jsonify({
            'success': True,
            'appointments': appointments_list,
            'count': len(appointments_list)
        }), 200
        
    except Exception as e:
        print(f"Error in get_user_appointments: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/appointments/<int:appointment_id>/status', methods=['PUT'])
@login_required
def update_appointment_status(appointment_id):
    """Update appointment status"""
    try:
        user_id = session.get('user_id')
        user_type = session.get('user_type')
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['pending', 'confirmed', 'cancelled', 'completed']:
            return jsonify({
                'success': False,
                'error': 'Invalid status'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user has permission (must be doctor or patient for their own appointment)
        cursor.execute('SELECT * FROM appointments WHERE id = ?', (appointment_id,))
        appointment = cursor.fetchone()
        
        if not appointment:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Appointment not found'
            }), 404
        
        appointment_dict = dict(appointment)
        
        # Verify permission
        if user_type == 'doctor' and appointment_dict['doctor_id'] != user_id:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 403
        elif user_type == 'patient' and appointment_dict['patient_id'] != user_id:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 403
        
        # Cannot cancel confirmed appointments
        if appointment_dict['status'] == 'confirmed' and new_status == 'cancelled':
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Cannot cancel confirmed appointments'
            }), 400
        
        # Update status
        print(f"Updating appointment {appointment_id} to status: {new_status}")  # Debug log
        print(f"Current appointment status: {appointment_dict['status']}")  # Debug log
        
        cursor.execute('''
            UPDATE appointments 
            SET status = ? 
            WHERE id = ?
        ''', (new_status, appointment_id))
        
        rows_affected = cursor.rowcount
        print(f"Rows affected by update: {rows_affected}")  # Debug log
        
        if rows_affected == 0:
            conn.rollback()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'No rows updated. Appointment may not exist or status is the same.'
            }), 400
        
        try:
            conn.commit()
            print(f"Committed update for appointment {appointment_id}")  # Debug log
            
            # Verify the update
            cursor.execute('SELECT status FROM appointments WHERE id = ?', (appointment_id,))
            updated_appointment = cursor.fetchone()
            if updated_appointment:
                print(f"Verified: Appointment {appointment_id} now has status: {updated_appointment['status']}")  # Debug log
        except Exception as commit_error:
            print(f"Error committing update: {str(commit_error)}")  # Debug log
            conn.rollback()
            conn.close()
            return jsonify({
                'success': False,
                'error': f'Failed to commit update: {str(commit_error)}'
            }), 500
        
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Appointment status updated',
            'appointment_id': appointment_id,
            'status': new_status
        }), 200
        
    except Exception as e:
        print(f"Error updating appointment status: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
@login_required
def delete_appointment(appointment_id):
    """Delete an appointment (only for pending appointments, cannot delete confirmed)"""
    try:
        user_id = session.get('user_id')
        user_type = session.get('user_type')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if appointment exists
        cursor.execute('SELECT * FROM appointments WHERE id = ?', (appointment_id,))
        appointment = cursor.fetchone()
        
        if not appointment:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Appointment not found'
            }), 404
        
        appointment_dict = dict(appointment)
        
        # Verify permission
        if user_type == 'doctor' and appointment_dict['doctor_id'] != user_id:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 403
        elif user_type == 'patient' and appointment_dict['patient_id'] != user_id:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 403
        
        # Cannot delete confirmed appointments
        if appointment_dict['status'] == 'confirmed':
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Cannot delete confirmed appointments'
            }), 400
        
        # Delete the appointment
        print(f"Deleting appointment {appointment_id}")  # Debug log
        print(f"Appointment status before delete: {appointment_dict['status']}")  # Debug log
        
        cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
        
        rows_affected = cursor.rowcount
        print(f"Rows affected by delete: {rows_affected}")  # Debug log
        
        if rows_affected == 0:
            conn.rollback()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'No rows deleted. Appointment may not exist.'
            }), 400
        
        try:
            conn.commit()
            print(f"Committed delete for appointment {appointment_id}")  # Debug log
            
            # Verify the delete (before closing connection)
            cursor.execute('SELECT * FROM appointments WHERE id = ?', (appointment_id,))
            deleted_check = cursor.fetchone()
            if deleted_check:
                print(f"WARNING: Appointment {appointment_id} still exists after delete!")  # Debug log
            else:
                print(f"Verified: Appointment {appointment_id} successfully deleted")  # Debug log
        except Exception as commit_error:
            print(f"Error committing delete: {str(commit_error)}")  # Debug log
            import traceback
            traceback.print_exc()
            conn.rollback()
            conn.close()
            return jsonify({
                'success': False,
                'error': f'Failed to commit delete: {str(commit_error)}'
            }), 500
        finally:
            conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Appointment deleted successfully'
        }), 200
        
    except Exception as e:
        print(f"Error deleting appointment: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== API Routes ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'MentIQ API is running',
        'ml_model_loaded': ML_PIPELINE is not None
    }), 200


@app.route('/api/consultation', methods=['POST'])
def submit_consultation():
    """Handle consultation booking submission and create appointment"""
    try:
        data = request.get_json()
        print(f"Consultation request data: {data}")  # Debug log
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'date', 'time', 'type', 'doctor_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Get user_id from session if logged in
        user_id = session.get('user_id')
        print(f"User ID from session: {user_id}")  # Debug log
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'You must be logged in to book an appointment'
            }), 401
        
        # Verify doctor exists
        conn = get_db_connection()
        cursor = conn.cursor()
        
        doctor_id = int(data['doctor_id'])
        print(f"Looking for doctor with user_id: {doctor_id}")  # Debug log
        
        cursor.execute('SELECT user_id FROM doctors WHERE user_id = ?', (doctor_id,))
        doctor = cursor.fetchone()
        
        if not doctor:
            conn.close()
            print(f"Doctor not found with user_id: {doctor_id}")  # Debug log
            return jsonify({
                'success': False,
                'error': 'Selected doctor not found'
            }), 404
        
        print(f"Doctor found: {doctor}")  # Debug log
        
        # Save consultation to database
        cursor.execute('''
            INSERT INTO consultations (user_id, name, email, phone, consultation_date, consultation_type, message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            data['name'],
            data['email'],
            data['phone'],
            data['date'],
            data['type'],
            data.get('message', '')
        ))
        
        consultation_id = cursor.lastrowid
        
        # Create appointment in appointments table
        cursor.execute('''
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, notes, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        ''', (
            user_id,
            doctor_id,
            data['date'],
            data['time'],
            f"Consultation Type: {data['type']}. {data.get('message', '')}"
        ))
        
        appointment_id = cursor.lastrowid
        print(f"Created appointment with ID: {appointment_id}, patient_id: {user_id}, doctor_id: {doctor_id}")  # Debug log
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Appointment booked successfully',
            'consultation_id': consultation_id,
            'appointment_id': appointment_id
        }), 201
        
    except Exception as e:
        print(f"Error in submit_consultation: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get mental health articles from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        category = request.args.get('category')
        
        if category:
            cursor.execute('''
                SELECT * FROM articles WHERE category = ?
                ORDER BY created_at DESC
            ''', (category,))
        else:
            cursor.execute('SELECT * FROM articles ORDER BY created_at DESC')
        
        articles = cursor.fetchall()
        conn.close()
        
        articles_list = [dict(article) for article in articles]
        
        return jsonify({
            'success': True,
            'articles': articles_list,
            'count': len(articles_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get list of doctors from database with optional filtering"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        country = request.args.get('country')
        city = request.args.get('city')
        specialty = request.args.get('specialty')
        
        query = 'SELECT * FROM doctors WHERE 1=1'
        params = []
        
        if country:
            query += ' AND country = ?'
            params.append(country)
        if city:
            query += ' AND city = ?'
            params.append(city)
        if specialty:
            query += ' AND specialty = ?'
            params.append(specialty)
        
        query += ' ORDER BY rating DESC, experience_years DESC'
        
        cursor.execute(query, params)
        doctors = cursor.fetchall()
        conn.close()
        
        doctors_list = [dict(doctor) for doctor in doctors]
        
        return jsonify({
            'success': True,
            'doctors': doctors_list,
            'count': len(doctors_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/assessment', methods=['POST'])
def submit_assessment():
    """Handle mental health assessment submission with ML model prediction"""
    try:
        data = request.get_json()
        
        # Map form data to ML model format
        # Get values from form, use defaults for missing fields
        age = data.get('age', 30)
        gender = data.get('gender', 'Other')
        sleep_hours = data.get('sleepHours', 7)
        physical_activity = data.get('physicalActivity', 3)
        screen_time = data.get('screenTime', 6)
        work_hours = data.get('workHours', 40)
        financial_stress = data.get('financialStress', 5)
        
        # Symptom flags (convert boolean to 0/1)
        feeling_nervous = 1 if data.get('feelingNervous', False) else 0
        trouble_concentrating = 1 if data.get('troubleConcentrating', False) else 0
        hopelessness = 1 if data.get('hopelessness', False) else 0
        anger = 1 if data.get('anger', False) else 0
        avoids_people = 1 if data.get('avoidsPeople', False) else 0
        nightmares = 1 if data.get('nightmares', False) else 0
        stressful_memories = 1 if data.get('stressfulMemories', False) else 0
        
        # Support system: form has 1 = yes (strong), 0 = no (limited)
        # Model expects score 1-10, so map: 1 -> 8 (strong), 0 -> 3 (limited)
        support_system_raw = data.get('supportSystem', 1)
        support_system = 8 if support_system_raw == 1 else 3
        
        family_history = data.get('familyHistory', 0)
        medication_usage = data.get('medicationUsage', 0)
        
        # Default values for fields not in assessment form
        employment_status = 'Employed'  # Default
        marital_status = 'Single'  # Default
        alcohol_units = 2  # Default moderate
        smoking_status = 'Never'  # Default
        chronic_condition = 0  # Default no
        stress_level = financial_stress  # Use financial stress as proxy
        rumination = 5  # Default moderate
        
        # Calculate rumination score based on symptoms
        symptom_count = feeling_nervous + trouble_concentrating + hopelessness + anger + avoids_people + nightmares + stressful_memories
        if symptom_count >= 5:
            rumination = 8
        elif symptom_count >= 3:
            rumination = 6
        else:
            rumination = 4
        
        # Prepare input for ML model
        input_data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender],
            'Employment_Status': [employment_status],
            'Marital_Status': [marital_status],
            'Work_Hours_per_Week': [work_hours],
            'Financial_Stress': [financial_stress],
            'Physical_Activity_Hours_per_Week': [physical_activity],
            'Screen_Time_per_Day_hours': [screen_time],
            'Sleep_Hours_per_Night': [sleep_hours],
            'Alcohol_Units_per_Week': [alcohol_units],
            'Smoking_Status': [smoking_status],
            'Family_History': [family_history],
            'Chronic_Condition': [chronic_condition],
            'Support_System_Score': [support_system],
            'Stress_Level_Score': [stress_level],
            'Rumination_Score': [rumination],
            'Feeling_Nervous': [feeling_nervous],
            'Trouble_Concentrating': [trouble_concentrating],
            'Hopelessness': [hopelessness],
            'Avoids_People': [avoids_people],
            'Nightmares': [nightmares],
            'Medication_Usage': [medication_usage]
        })
        
        # Make prediction using ML model
        prediction = None
        prediction_proba = None
        risk_score = 0
        risk_level = "Low"
        
        if ML_PIPELINE:
            try:
                prediction = ML_PIPELINE.predict(input_data)[0]
                prediction_proba = ML_PIPELINE.predict_proba(input_data)[0]
                
                # Convert prediction to risk score (0-100)
                # prediction_proba[1] is probability of being at risk
                risk_score = int(prediction_proba[1] * 100)
                
                # Determine risk level
                if risk_score <= 20:
                    risk_level = "Low"
                elif risk_score <= 40:
                    risk_level = "Moderate"
                elif risk_score <= 65:
                    risk_level = "High"
                else:
                    risk_level = "Very High"
                    
            except Exception as e:
                print(f"ML prediction error: {e}")
                # Fallback to simple calculation
                risk_score = calculate_fallback_risk(data)
                risk_level = get_risk_level_from_score(risk_score)
        else:
            # Fallback if model not available
            risk_score = calculate_fallback_risk(data)
            risk_level = get_risk_level_from_score(risk_score)
        
        # Generate risk factors and recommendations
        risk_factors = generate_risk_factors(data)
        recommendations = generate_recommendations(data, risk_score)
        
        # Save assessment to database if user is logged in
        user_id = session.get('user_id')
        if user_id:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO assessments (user_id, age, gender, risk_score, risk_level, prediction, prediction_probability, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id, age, gender, risk_score, risk_level, 
                    int(prediction) if prediction is not None else None,
                    float(prediction_proba[1]) if prediction_proba is not None else None,
                    datetime.now().isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error saving assessment: {e}")
        
        return jsonify({
            'success': True,
            'assessment': {
                'riskScore': risk_score,
                'riskLevel': risk_level,
                'prediction': int(prediction) if prediction is not None else None,
                'predictionProbability': float(prediction_proba[1]) if prediction_proba is not None else None,
                'riskFactors': risk_factors,
                'recommendations': recommendations
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def calculate_fallback_risk(data):
    """Fallback risk calculation if ML model unavailable"""
    score = 0
    
    # Sleep
    sleep = data.get('sleepHours', 7)
    if sleep <= 4:
        score += 40
    elif sleep <= 6:
        score += 20
    
    # Physical activity
    activity = data.get('physicalActivity', 3)
    if activity <= 1:
        score += 25
    elif activity <= 3:
        score += 10
    
    # Symptoms
    symptoms = [
        data.get('feelingNervous', False),
        data.get('troubleConcentrating', False),
        data.get('hopelessness', False),
        data.get('anger', False),
        data.get('avoidsPeople', False),
        data.get('nightmares', False),
        data.get('stressfulMemories', False)
    ]
    symptom_count = sum(symptoms)
    score += symptom_count * 8
    
    # Financial stress
    if data.get('financialStress', 5) >= 8:
        score += 15
    
    # Support system
    if data.get('supportSystem', 1) == 0:
        score += 15
    
    # Family history
    if data.get('familyHistory', 0) == 1:
        score += 12
    
    # Medication
    if data.get('medicationUsage', 0) == 1:
        score += 20
    
    return min(100, max(0, score))


def get_risk_level_from_score(score):
    """Get risk level from score"""
    if score <= 20:
        return "Low"
    elif score <= 40:
        return "Moderate"
    elif score <= 65:
        return "High"
    else:
        return "Very High"


def generate_risk_factors(data):
    """Generate list of identified risk factors"""
    factors = []
    
    sleep = data.get('sleepHours', 7)
    if sleep <= 4:
        factors.append("Severe sleep deprivation")
    elif sleep <= 6:
        factors.append("Insufficient sleep")
    
    activity = data.get('physicalActivity', 3)
    if activity <= 1:
        factors.append("Very low physical activity")
    elif activity <= 3:
        factors.append("Low physical activity")
    
    if data.get('feelingNervous', False):
        factors.append("Anxiety symptoms")
    if data.get('troubleConcentrating', False):
        factors.append("Concentration issues")
    if data.get('hopelessness', False):
        factors.append("Hopelessness")
    if data.get('anger', False):
        factors.append("Anger/irritability")
    if data.get('avoidsPeople', False):
        factors.append("Social avoidance")
    if data.get('nightmares', False):
        factors.append("Sleep disturbances")
    if data.get('stressfulMemories', False):
        factors.append("Intrusive memories")
    
    if data.get('financialStress', 5) >= 8:
        factors.append("High financial stress")
    
    support_system_raw = data.get('supportSystem', 1)
    if support_system_raw == 0:
        factors.append("Limited social support")
    
    if data.get('familyHistory', 0) == 1:
        factors.append("Family history of mental illness")
    
    if data.get('medicationUsage', 0) == 1:
        factors.append("Currently on mental health medication")
    
    return factors


def generate_recommendations(data, risk_score):
    """Generate personalized recommendations"""
    recommendations = []
    
    sleep = data.get('sleepHours', 7)
    if sleep <= 6:
        recommendations.append("🛏️ Prioritize 7-9 hours of sleep nightly - establish a consistent bedtime routine")
    
    activity = data.get('physicalActivity', 3)
    if activity <= 3:
        recommendations.append("🏃‍♂️ Increase physical activity to at least 150 minutes per week - start with daily walks")
    
    if data.get('workHours', 40) >= 50:
        recommendations.append("⚖️ Consider work-life balance strategies and stress management techniques")
    
    if data.get('financialStress', 5) >= 7:
        recommendations.append("💰 Explore financial counseling or budgeting resources to reduce financial stress")
    
    if data.get('screenTime', 6) >= 11:
        recommendations.append("📱 Reduce screen time, especially before bedtime, to improve sleep quality")
    
    support_system_raw = data.get('supportSystem', 1)
    if support_system_raw == 0:
        recommendations.append("🤝 Build social connections through community groups, therapy, or support networks")
    
    if data.get('feelingNervous', False) or data.get('troubleConcentrating', False):
        recommendations.append("🧘‍♀️ Practice mindfulness, deep breathing, or meditation for anxiety management")
    
    if data.get('hopelessness', False) or data.get('stressfulMemories', False):
        recommendations.append("💭 Consider professional counseling or therapy for emotional support")
    
    recommendations.append("📚 Explore our mental health articles and resources")
    recommendations.append("👨‍⚕️ Connect with qualified mental health professionals in our directory")
    
    if risk_score >= 40:
        recommendations.append("⚠️ Based on your assessment, we strongly recommend consulting with a mental health professional")
    
    return recommendations


@app.route('/api/appointments', methods=['POST'])
@login_required
def book_appointment():
    """Book an appointment with a doctor"""
    try:
        data = request.get_json()
        
        required_fields = ['doctor_id', 'appointment_date', 'appointment_time']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        patient_id = session.get('user_id')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            patient_id,
            data['doctor_id'],
            data['appointment_date'],
            data['appointment_time'],
            data.get('notes', '')
        ))
        
        appointment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Appointment booked successfully',
            'appointment_id': appointment_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Handle chatbot messages with ML model integration"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        user_id = session.get('user_id')
        
        # Try to use ML model for prediction
        risk_prediction = None
        response = None
        
        if ML_PIPELINE:
            try:
                # Extract features from message (simplified - in production, use NLP)
                # For now, use keyword-based feature extraction
                features = extract_features_from_message(message)
                
                if features:
                    # Create DataFrame with proper column names
                    input_df = pd.DataFrame([features])
                    
                    # Make prediction
                    prediction = ML_PIPELINE.predict(input_df)[0]
                    prediction_proba = ML_PIPELINE.predict_proba(input_df)[0]
                    
                    risk_prediction = float(prediction_proba[1])  # Probability of being at risk
                    
                    # Generate response based on prediction
                    if risk_prediction > 0.7:
                        response = "I'm concerned about what you've shared. Your message suggests you may benefit from speaking with a mental health professional. Would you like help finding a qualified therapist or counselor in your area? Remember, seeking help is a sign of strength."
                    elif risk_prediction > 0.4:
                        response = "Thank you for sharing. It sounds like you might be going through a challenging time. Consider exploring our mental health resources or speaking with a professional. I'm here to support you."
                    else:
                        response = generate_chatbot_response(message)  # Use fallback
                else:
                    response = generate_chatbot_response(message)  # Use fallback
                    
            except Exception as e:
                print(f"ML prediction error: {e}")
                response = generate_chatbot_response(message)  # Use fallback
        else:
            response = generate_chatbot_response(message)  # Use fallback
        
        # Save conversation to database
        if user_id:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO chatbot_conversations (user_id, message, response, risk_prediction)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, message, response, risk_prediction))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error saving conversation: {e}")
        
        return jsonify({
            'success': True,
            'response': response,
            'risk_prediction': risk_prediction
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def extract_features_from_message(message):
    """Extract features from message for ML model (simplified version)"""
    # This is a simplified feature extraction
    # In production, use proper NLP techniques
    
    message_lower = message.lower()
    
    # Basic feature extraction based on keywords
    features = {
        'Age': 30,  # Default
        'Gender': 'Other',
        'Employment_Status': 'Employed',
        'Marital_Status': 'Single',
        'Work_Hours_per_Week': 40,
        'Financial_Stress': 5,
        'Physical_Activity_Hours_per_Week': 3,
        'Screen_Time_per_Day_hours': 6,
        'Sleep_Hours_per_Night': 7,
        'Alcohol_Units_per_Week': 2,
        'Smoking_Status': 'Never',
        'Family_History': 0,
        'Chronic_Condition': 0,
        'Support_System_Score': 5,
        'Stress_Level_Score': 5,
        'Rumination_Score': 5,
        'Feeling_Nervous': 1 if any(w in message_lower for w in ['nervous', 'anxious', 'worried', 'panic']) else 0,
        'Trouble_Concentrating': 1 if any(w in message_lower for w in ['concentrate', 'focus', 'attention']) else 0,
        'Hopelessness': 1 if any(w in message_lower for w in ['hopeless', 'despair', 'no point']) else 0,
        'Avoids_People': 1 if any(w in message_lower for w in ['avoid', 'isolate', 'alone']) else 0,
        'Nightmares': 1 if any(w in message_lower for w in ['nightmare', 'dream', 'sleep']) else 0,
        'Medication_Usage': 0
    }
    
    # Adjust stress level based on message content
    if any(w in message_lower for w in ['stress', 'stressed', 'overwhelmed']):
        features['Stress_Level_Score'] = 8
    
    if any(w in message_lower for w in ['sad', 'depressed', 'depression', 'down']):
        features['Hopelessness'] = 1
        features['Stress_Level_Score'] = 7
    
    return features


def generate_chatbot_response(message):
    """Generate a response to user message (fallback when ML model unavailable)"""
    message_lower = message.lower()
    
    # Crisis keywords - prioritize these
    crisis_keywords = ['suicide', 'kill myself', 'end it all', 'self harm', 'hurt myself']
    for keyword in crisis_keywords:
        if keyword in message_lower:
            return "If you're having thoughts of self-harm or suicide, please reach out for immediate help: National Suicide Prevention Lifeline: 988 or text HOME to 741741. You are not alone, and there are people who want to help. Your life has value."
    
    if any(word in message_lower for word in ['sad', 'depressed', 'depression', 'down']):
        return "I understand you're going through a difficult time. It's important to remember that you're not alone. Have you considered speaking with a mental health professional? They can provide support and guidance tailored to your situation."
    
    elif any(word in message_lower for word in ['anxious', 'anxiety', 'worried', 'nervous', 'stress']):
        return "Anxiety can be overwhelming. Try some deep breathing exercises: inhale for 4 counts, hold for 4, and exhale for 4. If anxiety persists, consider reaching out to a therapist who specializes in anxiety disorders."
    
    elif any(word in message_lower for word in ['help', 'support', 'need']):
        return "I'm here to support you. Would you like to explore our articles, find a mental health professional, or discuss something specific? Remember, seeking professional help is a sign of strength."
    
    elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! 👋 I'm here to listen and support you. Please share what's on your mind, and I'll do my best to help."
    
    else:
        return "Thank you for sharing. I'm here to support you. If you're experiencing mental health concerns, I'd recommend speaking with a qualified mental health professional. Would you like help finding one in your area?"


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ==================== Main ====================

if __name__ == '__main__':
    # Initialize database
    print("Initializing database...")
    init_db()
    print("✅ Database initialized")
    
    # Run the Flask app
    print("Starting Flask server...")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True  # Set to False in production
    )
