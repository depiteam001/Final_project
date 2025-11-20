// ========== AUTHENTICATION SYSTEM ==========

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const userTypeSelect = document.getElementById('userType');
    const doctorFields = document.getElementById('doctorFields');

    // Show/hide doctor fields in register form
    if (userTypeSelect && doctorFields) {
        userTypeSelect.addEventListener('change', () => {
            doctorFields.style.display = userTypeSelect.value === 'doctor' ? 'block' : 'none';
        });
    }

    // Login form handler
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Register form handler
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const userType = document.getElementById('userType').value;

    // Simple validation
    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }

    // Get user data from registration or use email prefix as fallback
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const existingUser = users.find(u => u.email === email);
    
    const user = {
        email: email,
        name: existingUser ? existingUser.name : email.split('@')[0],
        type: userType,
        loginDate: new Date().toISOString()
    };

    localStorage.setItem('currentUser', JSON.stringify(user));
    localStorage.setItem('isLoggedIn', 'true');

    // Redirect based on user type
    if (userType === 'doctor') {
        window.location.href = 'doctor-dashboard.html';
    } else {
        window.location.href = 'index.html';
    }
}

function handleRegister(event) {
    event.preventDefault();
    
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const userType = document.getElementById('userType').value;
    const specialty = document.getElementById('specialty')?.value;
    const license = document.getElementById('license')?.value;

    // Validation
    if (!fullName || !email || !password) {
        alert('Please fill in all required fields');
        return;
    }

    if (userType === 'doctor' && (!specialty || !license)) {
        alert('Please fill in specialty and license number for doctor registration');
        return;
    }

    // Create user object
    const user = {
        email: email,
        name: fullName,
        type: userType,
        specialty: specialty,
        license: license,
        joinDate: new Date().toISOString(),
        patients: [],
        articles: []
    };

    // Save user data
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    users.push(user);
    localStorage.setItem('users', JSON.stringify(users));

    localStorage.setItem('currentUser', JSON.stringify(user));
    localStorage.setItem('isLoggedIn', 'true');

    alert('Registration successful!');

    // Redirect based on user type
    if (userType === 'doctor') {
        window.location.href = 'doctor-dashboard.html';
    } else {
        window.location.href = 'index.html';
    }
}