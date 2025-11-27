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

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail')?.value || document.getElementById('email')?.value;
    const password = document.getElementById('loginPassword')?.value || document.getElementById('password')?.value;
    const userType = document.getElementById('loginUserType')?.value || document.getElementById('userType')?.value;

    // Simple validation
    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',  // Important for session cookies
            body: JSON.stringify({
                email: email,
                password: password,
                user_type: userType
            })
        });

        const data = await response.json();

        if (data.success) {
            // Store user data in localStorage for frontend use
            localStorage.setItem('currentUser', JSON.stringify(data.user));
            localStorage.setItem('isLoggedIn', 'true');

            // Redirect based on user type
            if (userType === 'doctor') {
                window.location.href = 'doctor-dashboard.html';
            } else {
                window.location.href = 'index.html';
            }
        } else {
            alert('Login failed: ' + (data.error || 'Invalid credentials'));
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login. Please try again.');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const fullName = document.getElementById('registerName')?.value || document.getElementById('fullName')?.value;
    const email = document.getElementById('registerEmail')?.value || document.getElementById('email')?.value;
    const password = document.getElementById('registerPassword')?.value || document.getElementById('password')?.value;
    const userType = document.getElementById('registerUserType')?.value || document.getElementById('userType')?.value;
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

    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',  // Important for session cookies
            body: JSON.stringify({
                email: email,
                password: password,
                name: fullName,
                user_type: userType,
                specialty: specialty || null,
                license_number: license || null
            })
        });

        const data = await response.json();

        if (data.success) {
            // Store user data in localStorage for frontend use
            localStorage.setItem('currentUser', JSON.stringify(data.user));
            localStorage.setItem('isLoggedIn', 'true');

            alert('Registration successful!');

            // Redirect based on user type
            setTimeout(() => {
                if (userType === 'doctor') {
                    window.location.href = 'doctor-dashboard.html';
                } else {
                    window.location.href = 'index.html';
                }
            }, 500);
        } else {
            alert('Registration failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('An error occurred during registration. Please try again.');
    }
}