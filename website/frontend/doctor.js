// ========== DOCTOR DASHBOARD ==========

let currentDoctor = null;
let patients = [];
let doctorArticles = [];

document.addEventListener('DOMContentLoaded', () => {
    checkDoctorAuth();
    loadDoctorData();
    showSection('patients');
});

function checkDoctorAuth() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    
    if (!user || !isLoggedIn || user.type !== 'doctor') {
        window.location.href = 'login.html';
        return;
    }
    
    currentDoctor = user;
    document.getElementById('doctorName').textContent = `Dr. ${user.name}`;
}

function loadDoctorData() {
    // Load patients
    patients = JSON.parse(localStorage.getItem('patients') || '[]');
    
    // Load doctor's articles
    doctorArticles = JSON.parse(localStorage.getItem('doctorArticles') || '[]');
    
    updateStats();
    renderPatients();
    renderDoctorArticles();
    renderDoctorProfile();
}

function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionName).classList.add('active');
    
    // Update navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

function updateStats() {
    document.getElementById('totalPatients').textContent = patients.length;
    document.getElementById('todayAppointments').textContent = getTodayAppointments();
}

function getTodayAppointments() {
    const today = new Date().toDateString();
    return patients.filter(patient => 
        patient.appointments && 
        patient.appointments.some(apt => new Date(apt.date).toDateString() === today)
    ).length;
}

function renderPatients() {
    const container = document.getElementById('patientsContainer');
    
    if (patients.length === 0) {
        container.innerHTML = '<div class="empty-state">No patients registered yet.</div>';
        return;
    }
    
    container.innerHTML = patients.map(patient => `
        <div class="dashboard-card patient-card">
            <div class="card-header">
                <div class="card-icon">👤</div>
                <div class="card-title">${patient.name}</div>
            </div>
            <div class="patient-info">
                <p><strong>Email:</strong> ${patient.email}</p>
                <p><strong>Joined:</strong> ${new Date(patient.joinDate).toLocaleDateString()}</p>
                <p><strong>Last Visit:</strong> ${patient.lastVisit || 'Never'}</p>
                <p><strong>Status:</strong> <span class="status ${patient.status || 'active'}">${patient.status || 'Active'}</span></p>
            </div>
            <div class="patient-actions">
                <button class="btn btn-primary" onclick="viewPatient('${patient.id}')">View Details</button>
                <button class="btn btn-secondary" onclick="scheduleAppointment('${patient.id}')">Schedule</button>
            </div>
        </div>
    `).join('');
}

function renderDoctorArticles() {
    const container = document.getElementById('doctorArticles');
    
    if (doctorArticles.length === 0) {
        container.innerHTML = '<div class="empty-state">No articles created yet. Click "Add New Article" to get started.</div>';
        return;
    }
    
    container.innerHTML = doctorArticles.map(article => `
        <div class="article-card">
            <div class="article-header">${article.icon}</div>
            <div class="article-body">
                <div class="article-category">${article.category}</div>
                <div class="article-title">${article.title}</div>
                <div class="article-excerpt">${article.excerpt}</div>
                <div class="article-meta">
                    <small>By Dr. ${currentDoctor.name} • ${new Date(article.createdDate).toLocaleDateString()}</small>
                </div>
                <div class="article-actions">
                    <button class="btn btn-secondary" onclick="editArticle('${article.id}')">Edit</button>
                    <button class="btn btn-danger" onclick="deleteArticle('${article.id}')">Delete</button>
                </div>
            </div>
        </div>
    `).join('');
}

function renderDoctorProfile() {
    const container = document.getElementById('doctorProfile');
    
    container.innerHTML = `
        <div class="profile-info">
            <h3>Dr. ${currentDoctor.name}</h3>
            <p><strong>Email:</strong> ${currentDoctor.email}</p>
            <p><strong>Specialty:</strong> ${currentDoctor.specialty || 'General Practice'}</p>
            <p><strong>License:</strong> ${currentDoctor.license || 'N/A'}</p>
            <p><strong>Joined:</strong> ${new Date(currentDoctor.joinDate).toLocaleDateString()}</p>
            <p><strong>Total Patients:</strong> ${patients.length}</p>
            <p><strong>Articles Published:</strong> ${doctorArticles.length}</p>
        </div>
        <div class="profile-actions">
            <button class="btn btn-primary" onclick="editProfile()">Edit Profile</button>
        </div>
    `;
}

function showAddArticle() {
    document.getElementById('addArticleForm').style.display = 'block';
}

function hideAddArticle() {
    document.getElementById('addArticleForm').style.display = 'none';
    document.getElementById('addArticleForm').querySelector('form').reset();
}

function addArticle(event) {
    event.preventDefault();
    
    const title = document.getElementById('articleTitle').value;
    const category = document.getElementById('articleCategory').value;
    const excerpt = document.getElementById('articleExcerpt').value;
    const icon = document.getElementById('articleIcon').value || '📝';
    
    const article = {
        id: Date.now().toString(),
        title: title,
        category: category,
        excerpt: excerpt,
        icon: icon,
        author: currentDoctor.name,
        authorId: currentDoctor.email,
        createdDate: new Date().toISOString()
    };
    
    doctorArticles.push(article);
    localStorage.setItem('doctorArticles', JSON.stringify(doctorArticles));
    
    // Also add to main articles array
    const allArticles = JSON.parse(localStorage.getItem('articles') || '[]');
    allArticles.push(article);
    localStorage.setItem('articles', JSON.stringify(allArticles));
    
    hideAddArticle();
    renderDoctorArticles();
    alert('Article added successfully!');
}

function editArticle(articleId) {
    const article = doctorArticles.find(a => a.id === articleId);
    if (article) {
        document.getElementById('articleTitle').value = article.title;
        document.getElementById('articleCategory').value = article.category;
        document.getElementById('articleExcerpt').value = article.excerpt;
        document.getElementById('articleIcon').value = article.icon;
        showAddArticle();
        
        // Change form to edit mode
        const form = document.getElementById('addArticleForm').querySelector('form');
        form.onsubmit = (e) => updateArticle(e, articleId);
        form.querySelector('button[type="submit"]').textContent = 'Update Article';
    }
}

function updateArticle(event, articleId) {
    event.preventDefault();
    
    const articleIndex = doctorArticles.findIndex(a => a.id === articleId);
    if (articleIndex !== -1) {
        doctorArticles[articleIndex] = {
            ...doctorArticles[articleIndex],
            title: document.getElementById('articleTitle').value,
            category: document.getElementById('articleCategory').value,
            excerpt: document.getElementById('articleExcerpt').value,
            icon: document.getElementById('articleIcon').value,
            updatedDate: new Date().toISOString()
        };
        
        localStorage.setItem('doctorArticles', JSON.stringify(doctorArticles));
        hideAddArticle();
        renderDoctorArticles();
        alert('Article updated successfully!');
        
        // Reset form
        const form = document.getElementById('addArticleForm').querySelector('form');
        form.onsubmit = addArticle;
        form.querySelector('button[type="submit"]').textContent = 'Add Article';
    }
}

function deleteArticle(articleId) {
    if (confirm('Are you sure you want to delete this article?')) {
        doctorArticles = doctorArticles.filter(a => a.id !== articleId);
        localStorage.setItem('doctorArticles', JSON.stringify(doctorArticles));
        renderDoctorArticles();
        alert('Article deleted successfully!');
    }
}

function viewPatient(patientId) {
    const patient = patients.find(p => p.id === patientId);
    if (patient) {
        alert(`Patient Details:\n\nName: ${patient.name}\nEmail: ${patient.email}\nJoined: ${new Date(patient.joinDate).toLocaleDateString()}\nStatus: ${patient.status || 'Active'}`);
    }
}

function scheduleAppointment(patientId) {
    const date = prompt('Enter appointment date (YYYY-MM-DD):');
    const time = prompt('Enter appointment time (HH:MM):');
    
    if (date && time) {
        const patientIndex = patients.findIndex(p => p.id === patientId);
        if (patientIndex !== -1) {
            if (!patients[patientIndex].appointments) {
                patients[patientIndex].appointments = [];
            }
            
            patients[patientIndex].appointments.push({
                date: date,
                time: time,
                doctor: currentDoctor.name,
                status: 'scheduled'
            });
            
            localStorage.setItem('patients', JSON.stringify(patients));
            updateStats();
            alert('Appointment scheduled successfully!');
        }
    }
}

function editProfile() {
    alert('Profile editing feature coming soon!');
}

function logout() {
    localStorage.removeItem('currentUser');
    localStorage.removeItem('isLoggedIn');
    window.location.href = 'login.html';
}