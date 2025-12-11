# MentIQ Website Lifecycle & Features

## 🌐 Website Overview
MentIQ is a comprehensive mental health platform that connects patients with healthcare professionals, provides AI-powered risk assessment, educational content, and mental health support through multiple channels.

---

## 📋 User Lifecycle

### Phase 1: Initial Visit & Navigation
**What Happens:**
- User lands on the homepage (index.html)
- Navigation menu displays options: Home, Articles, Doctors, Chatbot, Motivation
- Theme toggle available (Light/Dark mode)
- User can browse without login

**Key Features Available:**
- 🏠 **Hero Section** - Welcome message and quick CTAs
- 📚 **Feature Cards** - Overview of platform capabilities
- 🌙 **Dark Mode** - Theme toggle for user preference

---

### Phase 2: Authentication & Registration

#### Option A: Patient Registration
**Process:**
1. User clicks "Login" → Redirected to login.html
2. Selects "Sign Up as Patient"
3. Fills in:
   - Email
   - Password
   - Full Name
   - User Type: Patient
4. Account created in SQLite database
5. Session established via cookies

#### Option B: Doctor Registration
**Process:**
1. User clicks "Login" → Redirected to login.html
2. Selects "Sign Up as Doctor"
3. Fills in:
   - Email
   - Password
   - Full Name
   - Medical Specialty
   - License Number
4. Account created with doctor verification fields
5. Session established

**API Endpoint:** `POST /api/auth/register`

---

### Phase 3: Patient Journey

#### Step 1: Mental Health Assessment
**Access:** Click "Take Assessment" button or navigate to assessment.html

**Assessment Form Includes:**
- **Basic Information**
  - Age (18-65)
  - Gender (Male / Female)

- **Lifestyle & Health**
  - Sleep hours per night
  - Physical activity hours per week
  - Screen time per day

- **Work & Financial Stress**
  - Work hours per week
  - Financial stress level (1-10 slider)

- **Current Symptoms** (Checkboxes)
  - Feeling nervous/anxious
  - Trouble concentrating
  - Hopelessness
  - Anger/Irritability
  - Avoids social situations
  - Nightmares
  - Intrusive stressful memories

- **Support & History**
  - Support system availability
  - Family history of mental health
  - Current medication usage

**Output:** Risk Assessment Results
- **Status:** "At Risk" or "Low Risk"
- **Risk Probability:** Percentage (0-100%)
- **Confidence Level:** Model confidence percentage
- **Contributing Factors:** Feature importance chart

#### Step 2: Explore Educational Content
**Access:** Navigate to "Articles" section

**Features:**
- Browse mental health articles
- Filter by category (Depression, Anxiety, etc.)
- Read detailed mental health information
- Educational resources for self-awareness

#### Step 3: Find Healthcare Professionals
**Access:** Navigate to "Doctors" section

**Features:**
- Browse available doctors
- Filter by:
  - Country
  - City
  - Specialty
- View doctor profiles
- Book appointments with doctors

**Appointment Booking:**
1. Select doctor
2. Submit consultation request
3. Wait for doctor confirmation
4. Once confirmed, appointment appears in profile

#### Step 4: AI Chatbot Support
**Access:** Navigate to "Chatbot" section

**Features:**
- Real-time chat interface
- ML-powered responses using trained mental health model
- Conversation history saved in database
- Provides supportive guidance and information
- 24/7 availability

#### Step 5: Motivation & Wellness
**Access:** Navigate to "Motivation" section (Flashcards)

**Features:**
- Daily motivation quotes
- Mental health tips
- Wellness flashcards
- Positive reinforcement content

#### Step 6: User Profile Management
**Access:** Click profile button (👤) in navigation

**Profile Features:**
- View personal information
- Edit profile details
- View assessment history
- Track booked appointments
- View confirmed appointments with doctors
- Manage preferences

---

### Phase 4: Doctor Journey

#### Doctor Dashboard
**Access:** doctor-dashboard.html (after doctor login)

**Key Metrics:**
- Total Appointments count
- Today's Appointments
- Pending Appointments (awaiting confirmation)
- Completed Appointments

**Features:**

1. **Appointments Management Section**
   - View all appointment requests
   - Patient name, email, date, time
   - Status badges: Pending, Confirmed, Completed, Cancelled
   - Actions available:
     - **For Pending:** Confirm or Delete
     - **For Confirmed:** Mark as Completed
     - **For Completed:** View only

2. **Doctor Profile**
   - Manage personal information
   - Update specialty details
   - View license information

3. **Navigation**
   - Dashboard tab (statistics)
   - Appointments tab (detailed list)
   - Profile tab (personal info)
   - Logout option

---

## 🗄️ Database Structure

### Tables:
1. **users** - All user accounts (patients & doctors)
2. **appointments** - Booked/confirmed appointments
3. **consultations** - Initial consultation requests
4. **articles** - Mental health educational content
5. **doctors** - Doctor profiles and specialties
6. **chatbot_conversations** - Chat history and interactions

---

## 🔧 Technical Features

### Backend (Flask API)
- **Authentication:** Session-based with password hashing
- **Database:** SQLite (lightweight, no external setup needed)
- **ML Integration:** Scikit-learn pipeline for risk assessment
- **REST API:** RESTful endpoints for all operations
- **CORS Enabled:** Cross-origin requests allowed

### Frontend
- **Responsive Design:** Mobile-first approach
- **Dark Mode:** User preference storage in localStorage
- **Interactive UI:** JavaScript event handling
- **API Communication:** Fetch-based async requests
- **State Management:** LocalStorage for user data

---

## 📡 API Endpoints Summary

### Authentication
```
POST   /api/auth/register      - User registration
POST   /api/auth/login         - User login
POST   /api/auth/logout        - User logout
GET    /api/auth/me            - Get current user (auth required)
```

### Frontend Routes
```
GET    /                       - Homepage
GET    /login                  - Login page
GET    /assessment             - Assessment page
GET    /doctor-dashboard       - Doctor dashboard (auth required)
GET    /profile                - User profile (auth required)
```

### Data Endpoints
```
GET    /api/articles           - Get mental health articles
GET    /api/doctors            - Get doctors list
POST   /api/appointments       - Book appointment (auth required)
GET    /api/profile/appointments - Get user's appointments (auth required)
PUT    /api/appointments/{id}/status - Update appointment status (auth required)
DELETE /api/appointments/{id}  - Delete appointment (auth required)
POST   /api/chatbot            - Send chatbot message
```

---

## 🎯 Key Features by User Type

### For Patients
✅ Self-assessment with AI risk evaluation
✅ Educational articles on mental health
✅ Find and book appointments with doctors
✅ AI chatbot for 24/7 support
✅ Motivation and wellness content
✅ Appointment tracking
✅ Profile management

### For Doctors
✅ View all patient appointment requests
✅ Confirm or deny appointments
✅ Mark appointments as completed
✅ Patient contact information
✅ Dashboard statistics
✅ Profile management

### For All Users
✅ Dark/Light theme toggle
✅ Secure authentication
✅ Responsive mobile design
✅ Session-based security
✅ Real-time data updates

---

## 🔐 Security Features
- Password hashing with industry-standard algorithms
- Session-based authentication
- CORS configuration for API security
- Login-required decorators for protected endpoints
- Input validation on all forms
- SQLite database with proper schema

---

## 📊 Data Flow

```
User Login
    ↓
Session Created
    ↓
Authentication Verified
    ↓
User Type Determined (Patient/Doctor)
    ↓
[PATIENT PATH] → Assessment → Results → Doctor Search → Booking
    ↓
[DOCTOR PATH] → Dashboard → Manage Appointments → Update Status
```

---

## 🚀 Deployment
- **Development:** `python app.py` (runs on localhost:5000)
- **Production:** Use Gunicorn or similar WSGI server
- **Database:** Automatically initialized on first run
- **ML Model:** Loads from `saved_models/full_pipeline.pkl`

---

## 📱 User Experience Highlights
1. **Intuitive Navigation** - Clear menu structure
2. **Mobile Responsive** - Works on all devices
3. **Fast Assessment** - Quick form completion
4. **Real-time Results** - Instant risk evaluation
5. **Accessible Design** - Dark mode support
6. **Secure Handling** - Encrypted authentication
7. **24/7 Support** - Chatbot always available

