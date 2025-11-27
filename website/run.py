"""
Simple script to run the Flask development server
"""
from app import app

if __name__ == '__main__':
    print("Starting MentIQ Flask API Server...")
    print("Server will be available at http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(host='0.0.0.0', port=5000, debug=True)

