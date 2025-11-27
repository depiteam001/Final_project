# MentIQ Flask API

Flask API server for the MentIQ Mental Health Platform with SQLite database, ML model integration, and authentication.

## Project Structure

```
website/
├── app.py              # Main Flask application
├── run.py              # Simple script to run the server
├── frontend/           # Frontend static files (HTML, CSS, JS)
│   ├── index.html
│   ├── login.html
│   ├── assessment.html
│   ├── doctor-dashboard.html
│   ├── style.css
│   ├── script.js       # Updated to call API endpoints
│   ├── auth.js         # Updated authentication
│   └── ...
├── backend/            # Backend models and utilities
│   ├── database.py     # SQLite database setup and models
│   └── models/
└── mentiq.db           # SQLite database (created on first run)
```

## Features

✅ **SQLite Database** - Lightweight, no external dependencies
✅ **Authentication** - Session-based authentication with password hashing
✅ **ML Model Integration** - Chatbot uses trained mental health prediction model
✅ **RESTful API** - All endpoints follow REST conventions
✅ **CORS Enabled** - Frontend can communicate with API

## Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

## Running the Server


### Development Mode

```bash
cd website
python app.py
```

The server will:
- Initialize the SQLite database on first run
- Load the ML model from `../saved_models/full_pipeline.pkl`
- Start on `http://localhost:5000`

### Production Mode

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Database Schema

The SQLite database includes:
- **users** - User accounts (patients and doctors)
- **consultations** - Consultation booking requests
- **articles** - Mental health articles
- **doctors** - Doctor profiles
- **appointments** - Booked appointments
- **chatbot_conversations** - Chatbot interaction history

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user (requires auth)

### Frontend Routes
- `GET /` - Main index page
- `GET /login` - Login page
- `GET /assessment` - Assessment page
- `GET /doctor-dashboard` - Doctor dashboard

### API Endpoints
- `GET /api/health` - Health check
- `POST /api/consultation` - Submit consultation booking
- `GET /api/articles` - Get articles (optional `?category=Depression`)
- `GET /api/doctors` - Get doctors (optional filters: `?country=Egypt&city=Cairo&specialty=Psychiatrist`)
- `POST /api/appointments` - Book appointment (requires auth)
- `POST /api/chatbot` - Chatbot message endpoint (uses ML model)

## Example API Usage

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe",
    "user_type": "patient"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Submit Consultation
```bash
curl -X POST http://localhost:5000/api/consultation \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "date": "2024-12-25",
    "type": "anxiety",
    "message": "I need help with anxiety"
  }'
```

### Get Articles
```bash
curl http://localhost:5000/api/articles
curl http://localhost:5000/api/articles?category=Depression
```

### Get Doctors
```bash
curl http://localhost:5000/api/doctors
curl http://localhost:5000/api/doctors?country=Egypt&city=Cairo
```

### Chatbot (with ML Model)
```bash
curl -X POST http://localhost:5000/api/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "I feel sad and hopeless"}'
```

## ML Model Integration

The chatbot endpoint uses the trained mental health prediction model:
- If ML model is available, it extracts features from the message and makes a risk prediction
- Responses are tailored based on the predicted risk level
- Falls back to keyword-based responses if ML model is unavailable

## Configuration

Set environment variables for production:
- `SECRET_KEY` - Flask secret key for sessions (required in production)
- `FLASK_ENV` - Set to `production` for production mode

## Notes

- The database is automatically initialized on first run
- Initial articles and doctors are seeded automatically
- Passwords are hashed using Werkzeug's password hashing
- Session-based authentication (cookies)
- ML model path: `../saved_models/full_pipeline.pkl`
- Database file: `website/mentiq.db`

## Frontend Updates

All frontend JavaScript has been updated to:
- Call API endpoints instead of using localStorage
- Handle authentication via API
- Display data from database
- Use ML-powered chatbot responses
