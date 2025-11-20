// ========== GLOBAL VARIABLES ==========
let currentPage = 'home';
let currentCardIndex = 0;
let isFlipped = false;
let selectedCategory = null;
let gameActive = true;
let selectedCardIndex = null;
let selectedCards = [];
let currentUser = null;
let isLoggedIn = false;

// ========== DATA ==========

// Articles Data
const articles = [
    { title: 'Understanding Depression', category: 'Depression', excerpt: 'Depression is more than sadness. Learn the signs and coping strategies.', icon: '🧠', link: 'https://www.mayoclinic.org/diseases-conditions/depression/symptoms-causes/syc-20356007', image: 'https://eudaimonic.co.uk/wp-content/uploads/2020/04/Therapy-Unlimited-Depression.jpg' },
    { title: 'Managing Anxiety Disorders', category: 'Anxiety', excerpt: 'Explore proven techniques to manage anxiety and panic attacks.', icon: '💙', link: 'https://www.medicalnewstoday.com/articles/323454', image: 'https://peninsulahealthcenter.com/wp-content/uploads/2023/09/shutterstock_1970640311-scaled.jpg' },
    { title: 'Bipolar Disorder Explained', category: 'Bipolar', excerpt: 'A comprehensive guide to understanding mood episodes and treatment.', icon: '🌙', link: 'https://en.wikipedia.org/wiki/Bipolar_disorder', image: 'https://4.bp.blogspot.com/-4PZF1lj6_pM/VDtcYDe4WCI/AAAAAAAAAZA/QXT56R50CZ0/s1600/34980b84dae10c2b4e30e80436dc9b25.jpg' },
    { title: 'PTSD Recovery Guide', category: 'PTSD', excerpt: 'Healing from trauma with evidence-based therapeutic approaches.', icon: '🕊️', link: 'https://neurolaunch.com/ptsd-recovery-stages/', image: 'https://therapymantra.co/wp-content/uploads/2022/04/ptsd.jpg' },
    { title: 'OCD Management Tips', category: 'OCD', excerpt: 'Understanding intrusive thoughts and breaking the cycle.', icon: '✨', link: 'https://www.treatmyocd.com/blog/6-best-strategies-to-combat-obsessive-compulsive-disorder', image: 'https://media.istockphoto.com/id/694068988/photo/obsessive-compulsive-disorder.webp?a=1&b=1&s=612x612&w=0&k=20&c=I5eq0QWRcXJZyEQL6ZGrq2_U0ndjt7YK1vO5blvJYcA=' },
    { title: 'ADHD in Adults', category: 'ADHD', excerpt: 'Recognizing ADHD symptoms and strategies for daily life.', icon: '⚡', link: 'https://www.healthline.com/health/adhd/adult-adhd', image: 'https://images.onlymyhealth.com/imported/images/2024/October/23_Oct_2024/mn-ADHD-adults.jpg' }
];

// Doctors Data
const doctors = [
    { name: 'Dr. Sarah Ahmed', specialty: 'Psychiatrist', country: 'Egypt', city: 'Cairo', rating: '4.8', experience: '12 years', avatar: '👩‍⚕️' },
    { name: 'Dr. James Wilson', specialty: 'Psychologist', country: 'USA', city: 'New York', rating: '4.9', experience: '10 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Fatima Hassan', specialty: 'Clinical Psychologist', country: 'Egypt', city: 'Alexandria', rating: '4.7', experience: '8 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Ahmed Karim', specialty: 'Psychiatrist', country: 'Egypt', city: 'Cairo', rating: '4.6', experience: '15 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Emily Brown', specialty: 'Psychologist', country: 'USA', city: 'New York', rating: '4.8', experience: '9 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Marcus Jones', specialty: 'Counselor', country: 'UK', city: 'London', rating: '4.7', experience: '7 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Leila Mostafa', specialty: 'Clinical Psychologist', country: 'Egypt', city: 'Giza', rating: '4.9', experience: '11 years', avatar: '👩‍⚕️' },
    { name: 'Dr. David Chen', specialty: 'Psychiatrist', country: 'USA', city: 'Los Angeles', rating: '4.8', experience: '13 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Sophia Garcia', specialty: 'Psychologist', country: 'USA', city: 'Miami', rating: '4.7', experience: '10 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Noor Al-Rashid', specialty: 'Counselor', country: 'UAE', city: 'Dubai', rating: '4.8', experience: '9 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Oliver Thompson', specialty: 'Psychiatrist', country: 'UK', city: 'Manchester', rating: '4.6', experience: '14 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Amara Okafor', specialty: 'Clinical Psychologist', country: 'UK', city: 'London', rating: '4.9', experience: '8 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Hassan El-Sayed', specialty: 'Psychologist', country: 'Egypt', city: 'Cairo', rating: '4.7', experience: '11 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Rachel Morrison', specialty: 'Counselor', country: 'USA', city: 'Chicago', rating: '4.8', experience: '7 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Khalid Al-Mansoori', specialty: 'Psychiatrist', country: 'UAE', city: 'Abu Dhabi', rating: '4.7', experience: '12 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Isabella Romano', specialty: 'Psychologist', country: 'UK', city: 'Liverpool', rating: '4.8', experience: '9 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Youssef Mansour', specialty: 'Clinical Psychologist', country: 'Egypt', city: 'Alexandria', rating: '4.6', experience: '10 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Anna Williams', specialty: 'Psychiatrist', country: 'USA', city: 'Boston', rating: '4.9', experience: '11 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Mohamed Ibrahim', specialty: 'Counselor', country: 'Egypt', city: 'Cairo', rating: '4.7', experience: '8 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Sarah Richardson', specialty: 'Psychologist', country: 'UK', city: 'Birmingham', rating: '4.8', experience: '10 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Amir Al-Hakim', specialty: 'Psychiatrist', country: 'UAE', city: 'Sharjah', rating: '4.6', experience: '13 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Jessica Turner', specialty: 'Clinical Psychologist', country: 'USA', city: 'Seattle', rating: '4.8', experience: '9 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Tarek Eldin', specialty: 'Counselor', country: 'Egypt', city: 'Giza', rating: '4.8', experience: '7 years', avatar: '👨‍⚕️' },
    { name: 'Dr. Nicole Dubois', specialty: 'Psychiatrist', country: 'UK', city: 'Leeds', rating: '4.7', experience: '12 years', avatar: '👩‍⚕️' },
    { name: 'Dr. Rashid Al-Kaabi', specialty: 'Psychologist', country: 'UAE', city: 'Dubai', rating: '4.9', experience: '11 years', avatar: '👨‍⚕️' }
];

// Motivation Cards Data
const motivationCards = [
    "You are stronger than you think, and braver than you feel.",
    "This moment will pass, and you will be okay.",
    "Your mental health matters just as much as your physical health.",
    "It's okay to not be okay sometimes. Healing takes time.",
    "Healing is not linear, and that's perfectly fine.",
    "You deserve kindness, especially from yourself.",
    "Small steps lead to big changes. Keep moving forward.",
    "Your story is not over yet. There are beautiful chapters ahead.",
    "Progress, not perfection. Every step counts.",
    "You are not alone in this journey. Support is always available.",
    "Be gentle with yourself today. You're doing the best you can.",
    "This too shall pass. Storms don't last forever.",
    "Every day is a fresh start and a new opportunity to grow.",
    "Your feelings are valid, and it's okay to feel them fully.",
    "You've survived 100% of your worst days. That's an amazing track record.",
    "Recovery is possible and worth fighting for. You are worth it.",
    "You matter more than you know. Your presence makes a difference.",
    "Tomorrow is a new opportunity to create positive change.",
    "Your courage to keep going inspires others, even when you don't see it.",
    "Self-care isn't selfish. It's necessary for your wellbeing.",
    "You have the power to rewrite your story, one day at a time.",
    "Asking for help is a sign of strength, not weakness.",
    "You are worthy of love, happiness, and all good things in life.",
    "Every breath you take is a victory. Keep breathing, keep fighting.",
    "Your struggles today are developing the strength you need for tomorrow.",
    "You don't have to be perfect to be amazing.",
    "Trust the process. Your current situation is not your final destination.",
    "You are capable of incredible things, even when you don't feel like it.",
    "Every small victory deserves to be celebrated.",
    "Your mental health journey is unique and valid.",
    "It's okay to rest. You don't always have to be productive.",
    "You are not broken. You are healing and growing.",
    "Your sensitivity is a superpower, not a weakness.",
    "You have survived difficult days before, and you can do it again."
];

// Chatbot Bot Responses
const botResponses = {
    'anxiety': 'Anxiety is a common experience that affects many people. Some effective techniques include deep breathing exercises, grounding techniques (5-4-3-2-1 method), and progressive muscle relaxation. Would you like me to guide you through a breathing exercise or connect you with professional resources?',
    'panic': 'Panic attacks can feel overwhelming, but they are temporary. Try the 4-7-8 breathing technique: breathe in for 4, hold for 7, exhale for 8. Remember, you are safe and this feeling will pass. If panic attacks are frequent, please consider speaking with a mental health professional.',
    'depression': 'Depression is a serious but treatable condition. It\'s important to know that you\'re not alone and help is available. Professional support from a therapist or psychiatrist can make a significant difference. Would you like information about finding mental health resources in your area?',
    'stress': 'Chronic stress can impact both mental and physical health. Effective stress management includes regular exercise, adequate sleep, mindfulness practices, and setting healthy boundaries. What specific stressors are you dealing with? I can suggest targeted coping strategies.',
    'sleep': 'Sleep difficulties often relate to mental health. Good sleep hygiene includes maintaining a consistent schedule, limiting screen time before bed, and creating a relaxing bedtime routine. If sleep problems persist, they may indicate underlying conditions that benefit from professional evaluation.',
    'trauma': 'Trauma responses are normal reactions to abnormal experiences. Healing is possible with proper support. Evidence-based treatments like EMDR and trauma-focused therapy have helped many people. Please consider reaching out to a trauma-informed mental health professional.',
    'bipolar': 'Bipolar disorder involves mood episodes that can significantly impact daily life. With proper treatment including medication and therapy, many people with bipolar disorder live fulfilling lives. It\'s important to work with a psychiatrist for accurate diagnosis and treatment planning.',
    'ocd': 'OCD involves intrusive thoughts and compulsive behaviors. Cognitive Behavioral Therapy (CBT) and Exposure Response Prevention (ERP) are highly effective treatments. Remember that having intrusive thoughts doesn\'t define you - they are symptoms that can be managed with professional help.',
    'ptsd': 'PTSD is a treatable condition that can develop after experiencing or witnessing trauma. Symptoms may include flashbacks, nightmares, and avoidance behaviors. Specialized therapies like EMDR and CPT have strong evidence for PTSD treatment. You deserve support in your healing journey.',
    'adhd': 'ADHD affects attention, hyperactivity, and impulse control. It\'s a neurodevelopmental condition that can be effectively managed with proper treatment, which may include therapy, medication, and lifestyle strategies. A comprehensive evaluation by a qualified professional is the first step.',
    'eating': 'Eating disorders are serious mental health conditions that require professional treatment. Recovery is possible with appropriate support including therapy, medical monitoring, and nutritional counseling. Please reach out to an eating disorder specialist or your healthcare provider.',
    'self harm': 'If you\'re having thoughts of self-harm, please reach out for immediate support. Contact a crisis helpline, go to your nearest emergency room, or call emergency services. You deserve care and support. These feelings can be addressed with professional help.',
    'suicide': 'If you\'re having thoughts of suicide, please reach out for immediate help: National Suicide Prevention Lifeline: 988 or text HOME to 741741. You are not alone, and there are people who want to help. Your life has value, and these feelings can change with proper support.',
    'crisis': 'If you\'re in immediate crisis, please contact emergency services (911) or go to your nearest emergency room. For mental health crisis support: National Crisis Text Line: Text HOME to 741741. You don\'t have to face this alone.',
    'therapy': 'Therapy can be incredibly beneficial for mental health. Different types include CBT (Cognitive Behavioral Therapy), DBT (Dialectical Behavior Therapy), and psychodynamic therapy. Finding the right therapist and approach may take time, but it\'s worth the investment in your wellbeing.',
    'medication': 'Psychiatric medications can be helpful tools in mental health treatment when prescribed by qualified professionals. They work best when combined with therapy and lifestyle changes. It\'s important to work closely with a psychiatrist to find the right medication and dosage for your specific needs.',
    'support': 'Having a strong support system is crucial for mental health. This can include family, friends, support groups, and mental health professionals. Don\'t hesitate to reach out - asking for help is a sign of strength, not weakness.',
    'coping': 'Healthy coping strategies include mindfulness meditation, regular exercise, journaling, creative activities, and connecting with others. It\'s important to develop a toolkit of strategies that work for you. What activities help you feel more grounded?',
    'help': 'I\'m here to provide information and support. You can explore our mental health articles, find qualified professionals in our directory, or continue our conversation. Remember, while I can offer general guidance, professional mental health support is important for personalized care.',
    'hello': 'Hello! Welcome to MentIQ. I\'m here to provide mental health information and support. How can I assist you today? You can ask about specific conditions, coping strategies, or finding professional help.',
    'hi': 'Hi there! I\'m glad you\'re here. Mental health is just as important as physical health, and seeking information shows strength. What would you like to know about or discuss today?',
    'thanks': 'You\'re very welcome. Remember, taking care of your mental health is an ongoing journey, and it\'s okay to seek support along the way. I\'m here whenever you need information or guidance.',
    'lonely': 'Feeling lonely is a common human experience, but persistent loneliness can impact mental health. Consider joining community groups, volunteering, or engaging in activities where you can meet like-minded people. If loneliness feels overwhelming, a therapist can help you develop connection strategies.',
    'anger': 'Anger is a normal emotion, but when it feels uncontrollable, it can benefit from professional attention. Anger management techniques include identifying triggers, using relaxation techniques, and developing healthy expression methods. Would you like some specific anger management strategies?'
};

// ========== NAVIGATION FUNCTIONS ==========

function navigateTo(pageName) {
    // Check if trying to access dashboard without being a logged-in patient
    if (pageName === 'dashboard') {
        checkLoginStatus();
        if (!isLoggedIn || !currentUser || currentUser.type !== 'patient') {
            showLoginRequired();
            return;
        }
    }
    
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));

    document.getElementById(pageName).classList.add('active');
    currentPage = pageName;

    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => btn.classList.remove('active'));
    
    const navButtonMap = {
        'home': 0,
        'articles': 1,
        'doctors': 2,
        'chatbot': 3,
        'flashcard': 4,
        'dashboard': 5
    };

    if (navButtonMap[pageName] !== undefined) {
        navBtns[navButtonMap[pageName]].classList.add('active');
    }

    closeMobileMenu();
    
    // Initialize page content when navigating
    if (pageName === 'articles') {
        renderCategoryFilters();
        filterArticles(null);
    } else if (pageName === 'doctors') {
        renderDoctors(doctors);
    } else if (pageName === 'dashboard') {
        initDashboard();
    }

    window.scrollTo(0, 0);
}

function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    navMenu.classList.toggle('active');
}

function closeMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    navMenu.classList.remove('active');
}

// ========== ARTICLES PAGE ==========

function renderCategoryFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    categoryFilter.innerHTML = '';

    const allBtn = document.createElement('button');
    allBtn.className = 'category-btn active';
    allBtn.textContent = 'All';
    allBtn.onclick = () => filterArticles(null);
    categoryFilter.appendChild(allBtn);

    const categories = [...new Set(articles.map(a => a.category))];
    categories.forEach(category => {
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.textContent = category;
        btn.onclick = () => filterArticles(category);
        categoryFilter.appendChild(btn);
    });
}

function filterArticles(category) {
    selectedCategory = category;
    const filtered = category ? articles.filter(a => a.category === category) : articles;
    
    const articlesGrid = document.getElementById('articlesGrid');
    articlesGrid.innerHTML = '';

    filtered.forEach(article => {
        const card = document.createElement('div');
        card.className = 'article-card';
        
        const header = document.createElement('div');
        header.className = 'article-header';
        header.style.backgroundImage = `url(${article.image})`;
        header.style.backgroundSize = 'cover';
        header.style.backgroundPosition = 'center';
        card.appendChild(header);

        const body = document.createElement('div');
        body.className = 'article-body';
        
        const categoryDiv = document.createElement('div');
        categoryDiv.className = 'article-category';
        categoryDiv.textContent = article.category;
        body.appendChild(categoryDiv);

        const titleDiv = document.createElement('div');
        titleDiv.className = 'article-title';
        titleDiv.textContent = article.title;
        body.appendChild(titleDiv);

        const excerptDiv = document.createElement('div');
        excerptDiv.className = 'article-excerpt';
        excerptDiv.textContent = article.excerpt;
        body.appendChild(excerptDiv);

        const readMore = document.createElement('div');
        readMore.className = 'read-more';
        const link = document.createElement('a');
        link.href = article.link;
        link.target = '_blank';
        link.textContent = 'Read More →';
        readMore.appendChild(link);
        
        const saveBtn = document.createElement('button');
        saveBtn.textContent = '❤️ Save';
        saveBtn.className = 'save-article-btn';
        saveBtn.onclick = () => saveArticle(article);
        readMore.appendChild(saveBtn);
        
        body.appendChild(readMore);

        card.appendChild(body);
        articlesGrid.appendChild(card);
    });

    const categoryBtns = document.querySelectorAll('.category-btn');
    categoryBtns.forEach(btn => {
        btn.classList.remove('active');
        if ((!category && btn.textContent === 'All') || (btn.textContent === category)) {
            btn.classList.add('active');
        }
    });
}

// ========== DOCTORS PAGE ==========

function applyDoctorFilters() {
    const country = document.getElementById('countryFilter').value;
    const city = document.getElementById('cityFilter').value;
    const specialty = document.getElementById('specialtyFilter').value;

    const filtered = doctors.filter(doctor => {
        return (!country || doctor.country === country) &&
               (!city || doctor.city === city) &&
               (!specialty || doctor.specialty === specialty);
    });

    renderDoctors(filtered);
}

function renderDoctors(doctorsList) {
    const doctorsContainer = document.getElementById('doctorsList');
    doctorsContainer.innerHTML = '';

    if (doctorsList.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.textContent = 'No doctors found matching your criteria.';
        doctorsContainer.appendChild(emptyState);
        return;
    }

    doctorsList.forEach(doctor => {
        const card = document.createElement('div');
        card.className = 'doctor-card';

        const avatar = document.createElement('div');
        avatar.className = 'doctor-avatar';
        avatar.textContent = doctor.avatar;
        card.appendChild(avatar);

        const info = document.createElement('div');
        info.className = 'doctor-info';

        const name = document.createElement('div');
        name.className = 'doctor-name';
        name.textContent = doctor.name;
        info.appendChild(name);

        const specialty = document.createElement('div');
        specialty.className = 'doctor-specialty';
        specialty.textContent = doctor.specialty;
        info.appendChild(specialty);

        const details = document.createElement('div');
        details.className = 'doctor-details';
        details.innerHTML = `
            <span>📍 ${doctor.city}, ${doctor.country}</span>
            <span>⏱️ ${doctor.experience}</span>
            <span class="doctor-rating">⭐ ${doctor.rating}</span>
        `;
        info.appendChild(details);

        card.appendChild(info);

        const actions = document.createElement('div');
        actions.className = 'doctor-actions';

        const bookBtn = document.createElement('button');
        bookBtn.className = 'action-btn';
        bookBtn.textContent = '📅 Book';
        bookBtn.onclick = () => bookDoctor(doctor);
        actions.appendChild(bookBtn);

        const callBtn = document.createElement('button');
        callBtn.className = 'action-btn';
        callBtn.textContent = '📞 Call';
        callBtn.onclick = () => contactDoctor(doctor.name, 'call');
        actions.appendChild(callBtn);

        const saveBtn = document.createElement('button');
        saveBtn.className = 'action-btn';
        saveBtn.textContent = '❤️ Save';
        saveBtn.onclick = () => saveDoctor(doctor.name);
        actions.appendChild(saveBtn);

        card.appendChild(actions);
        doctorsContainer.appendChild(card);
    });
}

function contactDoctor(doctorName, type) {
    const action = type === 'call' ? 'Calling' : 'Messaging';
    alert(`${action} Dr. ${doctorName}...`);
}

function bookDoctor(doctor) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.5); display: flex; align-items: center;
        justify-content: center; z-index: 1000;
    `;
    
    modal.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 20px; max-width: 500px; width: 90%;">
            <h3 style="color: #00695c; margin-bottom: 20px;">Book Appointment with ${doctor.name}</h3>
            <form id="bookingForm">
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600;">Doctor:</label>
                    <input type="text" value="${doctor.name}" readonly style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px; background: #f5f5f5;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600;">Location:</label>
                    <input type="text" value="${doctor.city}, ${doctor.country}" readonly style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px; background: #f5f5f5;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600;">Patient Name:</label>
                    <input type="text" id="patientName" required style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600;">Date:</label>
                    <input type="date" id="appointmentDate" required style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600;">Time:</label>
                    <select id="appointmentTime" required style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px;">
                        <option value="">Select time</option>
                        <option value="09:00">09:00 AM</option>
                        <option value="10:00">10:00 AM</option>
                        <option value="11:00">11:00 AM</option>
                        <option value="14:00">02:00 PM</option>
                        <option value="15:00">03:00 PM</option>
                        <option value="16:00">04:00 PM</option>
                    </select>
                </div>
                <div style="display: flex; gap: 10px; justify-content: flex-end;">
                    <button type="button" onclick="this.closest('div').parentElement.remove()" style="padding: 10px 20px; border: 2px solid #00897b; background: white; color: #00897b; border-radius: 8px; cursor: pointer;">Cancel</button>
                    <button type="submit" style="padding: 10px 20px; background: #00897b; color: white; border: none; border-radius: 8px; cursor: pointer;">Book Appointment</button>
                </div>
            </form>
        </div>
    `;
    
    modal.querySelector('#bookingForm').onsubmit = (e) => {
        e.preventDefault();
        const booking = {
            doctor: doctor.name,
            location: `${doctor.city}, ${doctor.country}`,
            patientName: modal.querySelector('#patientName').value,
            date: modal.querySelector('#appointmentDate').value,
            time: modal.querySelector('#appointmentTime').value,
            status: 'pending',
            bookedAt: new Date().toISOString()
        };
        
        const bookings = JSON.parse(localStorage.getItem('doctorBookings') || '[]');
        bookings.push(booking);
        localStorage.setItem('doctorBookings', JSON.stringify(bookings));
        
        alert(`Appointment booked with ${doctor.name} on ${booking.date} at ${booking.time}`);
        modal.remove();
    };
    
    document.body.appendChild(modal);
}

function saveDoctor(doctorName) {
    alert(`Saved Dr. ${doctorName} to your favorites!`);
}

// ========== CHATBOT PAGE ==========

function handleChatKeypress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

function sendChatMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();

    if (message === '') return;

    const chatMessages = document.getElementById('chatMessages');

    const userMsg = document.createElement('div');
    userMsg.className = 'message user-message';
    userMsg.textContent = message;
    chatMessages.appendChild(userMsg);

    chatInput.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;

    setTimeout(() => {
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot-message';
        botMsg.textContent = getBotResponse(message);
        chatMessages.appendChild(botMsg);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 500);
}

function getBotResponse(message) {
    const lowerMessage = message.toLowerCase();

    // Check for multiple keywords and prioritize crisis responses
    const crisisKeywords = ['suicide', 'kill myself', 'end it all', 'self harm', 'hurt myself'];
    for (let keyword of crisisKeywords) {
        if (lowerMessage.includes(keyword)) {
            return botResponses['suicide'] || botResponses['crisis'];
        }
    }

    // Check for other keywords
    for (let keyword in botResponses) {
        if (lowerMessage.includes(keyword)) {
            return botResponses[keyword];
        }
    }

    // Default professional response
    return 'Thank you for reaching out. Mental health is important, and I\'m here to help with information and resources. You can ask me about specific mental health conditions, coping strategies, or finding professional support. What would you like to know more about?';
}

// ========== FLASHCARD PAGE ==========

function shuffleCards() {
    const shuffled = [...motivationCards].sort(() => 0.5 - Math.random());
    window.selectedCards = shuffled.slice(0, 3);
    window.gameActive = true;
    window.selectedCardIndex = null;
}

function addCardHoverEffects() {
    const cards = document.querySelectorAll('.flashcard');
    
    cards.forEach((card, index) => {
        card.addEventListener('mouseenter', () => {
            if (window.gameActive) {
                card.style.transform = getCardTransform(index, true);
            }
        });
        
        card.addEventListener('mouseleave', () => {
            if (window.gameActive && !card.classList.contains('selected')) {
                card.style.transform = getCardTransform(index, false);
            }
        });
    });
}

function getCardTransform(index, isHover) {
    const baseTransforms = {
        0: isHover ? 'translateY(-15px) rotateY(-10deg) scale(1.05)' : 'rotateY(-15deg)',
        1: isHover ? 'translateY(-15px) scale(1.15)' : 'scale(1.1)',
        2: isHover ? 'translateY(-15px) rotateY(10deg) scale(1.05)' : 'rotateY(15deg)'
    };
    return baseTransforms[index];
}

function selectCard(position) {
    if (!window.gameActive) return;

    window.gameActive = false;
    window.selectedCardIndex = position;

    const cards = document.querySelectorAll('.flashcard');
    const selectedCard = cards[position];
    
    cards.forEach((card, index) => {
        if (index !== position) {
            card.style.opacity = '0.3';
            card.style.transform = 'translateY(20px) scale(0.8)';
            card.style.pointerEvents = 'none';
        }
    });
    
    selectedCard.classList.add('selected');
    selectedCard.style.transform = 'scale(1.2) rotateY(360deg)';
    
    setTimeout(() => {
        showRevealedMessage(position);
        updateStreak();
    }, 800);
}

function showRevealedMessage(cardIndex) {
    const messageContainer = document.getElementById('messageContainer');
    const selectedMessage = window.selectedCards[cardIndex];

    const revealedMsg = document.createElement('div');
    revealedMsg.className = 'revealed-message';

    const title = document.createElement('h3');
    title.textContent = '✨ Your Daily Motivation ✨';
    revealedMsg.appendChild(title);

    const text = document.createElement('p');
    text.textContent = `"${selectedMessage}"`;
    revealedMsg.appendChild(text);

    messageContainer.appendChild(revealedMsg);

    setTimeout(() => {
        document.getElementById('gameButtons').style.display = 'flex';
    }, 300);
}

function resetGame() {
    window.selectedCardIndex = null;
    window.gameActive = true;
    
    const messageContainer = document.getElementById('messageContainer');
    messageContainer.innerHTML = '';
    
    document.getElementById('gameButtons').style.display = 'none';

    const cards = document.querySelectorAll('.flashcard');
    const cardIcons = ['✨', '💫', '⭐'];
    
    cards.forEach((card, index) => {
        card.classList.remove('selected');
        card.textContent = cardIcons[index];
        card.style.opacity = '1';
        card.style.pointerEvents = 'auto';
        card.style.transform = getCardTransform(index, false);
    });

    shuffleCards();
    addCardHoverEffects();
}

function saveSelectedCard() {
    if (window.selectedCardIndex !== null) {
        const message = window.selectedCards[window.selectedCardIndex];
        const savedMessages = JSON.parse(localStorage.getItem('savedMotivations') || '[]');
        
        if (!savedMessages.includes(message)) {
            savedMessages.push(message);
            localStorage.setItem('savedMotivations', JSON.stringify(savedMessages));
            alert(`💾 Message saved successfully!\n\n"${message}"\n\nYou now have ${savedMessages.length} saved messages.`);
        } else {
            alert('📝 This message is already in your saved collection!');
        }
    }
}

function getStreak() {
    const lastPlayed = localStorage.getItem('lastMotivationDate');
    const today = new Date().toDateString();
    const streak = parseInt(localStorage.getItem('motivationStreak') || '0');
    
    if (lastPlayed === today) {
        return streak;
    }
    
    return streak;
}

function updateStreak() {
    const today = new Date().toDateString();
    const lastPlayed = localStorage.getItem('lastMotivationDate');
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayStr = yesterday.toDateString();
    
    let currentStreak = parseInt(localStorage.getItem('motivationStreak') || '0');
    
    if (lastPlayed === today) {
        return;
    } else if (lastPlayed === yesterdayStr) {
        currentStreak += 1;
    } else if (lastPlayed !== yesterdayStr && lastPlayed !== null) {
        currentStreak = 1;
    } else {
        currentStreak = 1;
    }
    
    localStorage.setItem('motivationStreak', currentStreak.toString());
    localStorage.setItem('lastMotivationDate', today);
    
    const streakElement = document.getElementById('streakCount');
    if (streakElement) {
        streakElement.textContent = currentStreak;
    }
    
    if (currentStreak > 1 && currentStreak % 5 === 0) {
        setTimeout(() => {
            alert(`🎉 Amazing! You've reached a ${currentStreak}-day streak! Keep it up!`);
        }, 1000);
    }
}

// ========== DARK MODE TOGGLE ==========

function toggleTheme() {
    const body = document.body;
    const themeToggle = document.getElementById('themeToggle');
    
    body.classList.toggle('dark-mode');
    
    const isDarkMode = body.classList.contains('dark-mode');
    const icon = isDarkMode ? '☀️' : '🌙';
    
    if (themeToggle) themeToggle.textContent = icon;
    
    localStorage.setItem('darkMode', isDarkMode);
}

function loadTheme() {
    const savedTheme = localStorage.getItem('darkMode');
    const themeToggle = document.getElementById('themeToggle');
    
    if (savedTheme === 'true') {
        document.body.classList.add('dark-mode');
        if (themeToggle) themeToggle.textContent = '☀️';
    }
}

// ========== CONSULTATION FORM ==========

function submitConsultation(event) {
    event.preventDefault();
    
    const name = document.getElementById('contactName').value;
    const email = document.getElementById('contactEmail').value;
    const phone = document.getElementById('contactPhone').value;
    const date = document.getElementById('consultationDate').value;
    const type = document.getElementById('consultationType').value;
    const message = document.getElementById('consultationMessage').value;
    
    const consultation = {
        id: Date.now().toString(),
        name: name,
        email: email,
        phone: phone,
        date: date,
        type: type,
        message: message,
        status: 'pending',
        submittedAt: new Date().toISOString()
    };
    
    const consultations = JSON.parse(localStorage.getItem('consultations') || '[]');
    consultations.push(consultation);
    localStorage.setItem('consultations', JSON.stringify(consultations));
    
    alert('🎉 Consultation request submitted successfully!\n\nWe will contact you within 24 hours to confirm your appointment.');
    
    event.target.reset();
}

// ========== INITIALIZE ON LOAD ==========

function initDashboard() {
    const dashboardPage = document.getElementById('dashboard');
    
    const bookings = JSON.parse(localStorage.getItem('doctorBookings') || '[]');
    const savedArticles = JSON.parse(localStorage.getItem('savedArticles') || '[]');
    const savedMotivations = JSON.parse(localStorage.getItem('savedMotivations') || '[]');
    const assessment = JSON.parse(localStorage.getItem('mentalHealthAssessment') || 'null');
    
    dashboardPage.innerHTML = `
        <h2 class="page-title">📈 My Dashboard</h2>
        
        <div class="dashboard-grid">
            ${assessment ? `
                <div class="dashboard-section">
                    <h3>🧠 Mental Health Assessment</h3>
                    <div class="assessment-summary">
                        <div class="risk-indicator ${assessment.riskLevel.toLowerCase()}">
                            <span class="risk-level">${assessment.riskLevel} Risk</span>
                            <span class="risk-score">${assessment.riskScore}/100</span>
                        </div>
                        <p class="assessment-date">Completed: ${new Date(assessment.assessmentDate).toLocaleDateString()}</p>
                        <button class="btn btn-secondary" onclick="window.location.href='assessment.html'">Retake Assessment</button>
                    </div>
                </div>
            ` : `
                <div class="dashboard-section">
                    <h3>🧠 Mental Health Assessment</h3>
                    <div class="assessment-prompt">
                        <p>Take our comprehensive mental health assessment to get personalized recommendations.</p>
                        <button class="btn btn-primary" onclick="window.location.href='assessment.html'">Take Assessment</button>
                    </div>
                </div>
            `}
            
            <div class="dashboard-section">
                <h3>📅 My Appointments</h3>
                <div class="appointments-list">
                    ${bookings.length ? bookings.map(booking => `
                        <div class="appointment-card">
                            <div class="appointment-info">
                                <h4>${booking.doctor}</h4>
                                <p>📍 ${booking.location}</p>
                                <p>📅 ${booking.date} at ${booking.time}</p>
                                <span class="status ${booking.status}">${booking.status}</span>
                            </div>
                        </div>
                    `).join('') : '<p class="empty-message">No appointments booked yet</p>'}
                </div>
            </div>
            
            <div class="dashboard-section">
                <h3>❤️ Saved Articles</h3>
                <div class="saved-articles">
                    ${savedArticles.length ? savedArticles.map(article => `
                        <div class="saved-item">
                            <h4>${article.title}</h4>
                            <p>${article.category}</p>
                            <a href="${article.link}" target="_blank" class="read-link">Read Article →</a>
                        </div>
                    `).join('') : '<p class="empty-message">No articles saved yet</p>'}
                </div>
            </div>
            
            <div class="dashboard-section">
                <h3>✨ Saved Motivations</h3>
                <div class="saved-motivations">
                    ${savedMotivations.length ? savedMotivations.map(message => `
                        <div class="motivation-item">
                            <p>"${message}"</p>
                        </div>
                    `).join('') : '<p class="empty-message">No motivations saved yet</p>'}
                </div>
            </div>
        </div>
    `;
}

function isUserLoggedIn() {
    return localStorage.getItem('currentUser') !== null && localStorage.getItem('isLoggedIn') === 'true';
}

function showLoginRequired() {
    const dashboardPage = document.getElementById('dashboard');
    dashboardPage.innerHTML = `
        <div style="text-align: center; padding: 50px;">
            <h2 style="color: #00695c; margin-bottom: 20px;">🔒 Patient Login Required</h2>
            <p style="margin-bottom: 30px; color: #666;">Please log in as a patient to access your dashboard</p>
            <a href="login.html" class="btn btn-primary">Go to Login</a>
        </div>
    `;
}

function updateNavigation() {
    checkLoginStatus();
    const dashboardNav = document.getElementById('dashboardNav');
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    
    if (isLoggedIn && currentUser && currentUser.type === 'patient') {
        dashboardNav.style.display = 'block';
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'inline-block';
        showWelcomePopup();
    } else {
        dashboardNav.style.display = 'none';
        loginBtn.style.display = 'inline-block';
        logoutBtn.style.display = 'none';
    }
}

function showWelcomePopup() {
    const popup = document.createElement('div');
    popup.style.cssText = `
        position: fixed; top: 20px; right: 20px; z-index: 2000;
        background: linear-gradient(135deg, #00897b, #4db6ac);
        color: white; padding: 15px 20px; border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0, 137, 123, 0.3);
        font-weight: 600; animation: slideInRight 0.5s ease;
    `;
    popup.innerHTML = `🎉 Welcome back, ${currentUser.name}! Great to see you again!`;
    
    document.body.appendChild(popup);
    
    setTimeout(() => {
        popup.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => popup.remove(), 500);
    }, 3000);
}

function checkLoginStatus() {
    const userData = localStorage.getItem('currentUser');
    const loginStatus = localStorage.getItem('isLoggedIn');
    
    if (userData && loginStatus === 'true') {
        currentUser = JSON.parse(userData);
        isLoggedIn = true;
    } else {
        currentUser = null;
        isLoggedIn = false;
    }
}

function logout() {
    localStorage.removeItem('currentUser');
    localStorage.removeItem('isLoggedIn');
    currentUser = null;
    isLoggedIn = false;
    updateNavigation();
    
    if (currentPage === 'dashboard') {
        navigateTo('home');
    }
    
    alert('You have been logged out successfully.');
}

function saveArticle(article) {
    const savedArticles = JSON.parse(localStorage.getItem('savedArticles') || '[]');
    if (!savedArticles.find(a => a.title === article.title)) {
        savedArticles.push(article);
        localStorage.setItem('savedArticles', JSON.stringify(savedArticles));
        alert('Article saved to your dashboard!');
    } else {
        alert('Article already saved!');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    shuffleCards();
    addCardHoverEffects();
    checkLoginStatus();
    updateNavigation();
});