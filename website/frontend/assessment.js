// Mental Health Assessment Logic based on ML model insights

function updateSliderValue(sliderId) {
    const slider = document.getElementById(sliderId);
    const valueSpan = document.getElementById(sliderId + 'Value');
    valueSpan.textContent = slider.value;
}

function calculateRiskScore(formData) {
    let riskScore = 0;
    let riskFactors = [];

    // Sleep Hours (strongest predictor)
    if (formData.sleepHours <= 4) {
        riskScore += 40; // Very high risk
        riskFactors.push("Severe sleep deprivation");
    } else if (formData.sleepHours <= 6) {
        riskScore += 20; // Moderate risk
        riskFactors.push("Insufficient sleep");
    } else if (formData.sleepHours >= 10) {
        riskScore -= 10; // Protective
    }

    // Physical Activity (strong protective factor)
    if (formData.physicalActivity <= 1) {
        riskScore += 25;
        riskFactors.push("Very low physical activity");
    } else if (formData.physicalActivity <= 3) {
        riskScore += 10;
        riskFactors.push("Low physical activity");
    } else if (formData.physicalActivity >= 10) {
        riskScore -= 15; // Highly protective
    }

    // Work Hours & Financial Stress combination
    if (formData.workHours >= 50 && formData.financialStress >= 7) {
        riskScore += 30;
        riskFactors.push("High work stress and financial pressure");
    } else if (formData.workHours >= 65) {
        riskScore += 20;
        riskFactors.push("Excessive work hours");
    }

    if (formData.financialStress >= 8) {
        riskScore += 15;
        riskFactors.push("High financial stress");
    }

    // Screen Time (moderate factor)
    if (formData.screenTime >= 14) {
        riskScore += 10;
        riskFactors.push("Excessive screen time");
    }

    // Symptom clusters (high predictive value)
    let symptomCount = 0;
    if (formData.feelingNervous) { symptomCount++; riskFactors.push("Anxiety symptoms"); }
    if (formData.troubleConcentrating) { symptomCount++; riskFactors.push("Concentration issues"); }
    if (formData.hopelessness) { symptomCount++; riskFactors.push("Hopelessness"); }
    if (formData.anger) { symptomCount++; riskFactors.push("Anger/irritability"); }
    if (formData.avoidsPeople) { symptomCount++; riskFactors.push("Social avoidance"); }
    if (formData.nightmares) { symptomCount++; riskFactors.push("Sleep disturbances"); }
    if (formData.stressfulMemories) { symptomCount++; riskFactors.push("Intrusive memories"); }

    riskScore += symptomCount * 8; // Each symptom adds significant risk

    // Family History
    if (formData.familyHistory == 1) {
        riskScore += 12;
        riskFactors.push("Family history of mental illness");
    }

    // Support System (protective)
    if (formData.supportSystem == 0) {
        riskScore += 15;
        riskFactors.push("Limited social support");
    } else {
        riskScore -= 8; // Protective factor
    }

    // Current medication (indicates existing condition)
    if (formData.medicationUsage == 1) {
        riskScore += 20;
        riskFactors.push("Currently on mental health medication");
    }

    return { score: Math.max(0, Math.min(100, riskScore)), factors: riskFactors };
}

function getRiskLevel(score) {
    if (score <= 20) return { level: "Low", color: "#4caf50", description: "Your responses suggest good mental health with minimal risk factors." };
    if (score <= 40) return { level: "Moderate", color: "#ff9800", description: "Some risk factors present. Consider lifestyle improvements and monitoring." };
    if (score <= 65) return { level: "High", color: "#f44336", description: "Multiple risk factors identified. Professional consultation recommended." };
    return { level: "Very High", color: "#d32f2f", description: "Significant risk factors present. Immediate professional support strongly recommended." };
}

function generateRecommendations(formData, riskFactors) {
    let recommendations = [];

    // Sleep recommendations
    if (formData.sleepHours <= 6) {
        recommendations.push("🛏️ Prioritize 7-9 hours of sleep nightly - establish a consistent bedtime routine");
    }

    // Physical activity
    if (formData.physicalActivity <= 3) {
        recommendations.push("🏃‍♂️ Increase physical activity to at least 150 minutes per week - start with daily walks");
    }

    // Work-life balance
    if (formData.workHours >= 50) {
        recommendations.push("⚖️ Consider work-life balance strategies and stress management techniques");
    }

    // Financial stress
    if (formData.financialStress >= 7) {
        recommendations.push("💰 Explore financial counseling or budgeting resources to reduce financial stress");
    }

    // Screen time
    if (formData.screenTime >= 11) {
        recommendations.push("📱 Reduce screen time, especially before bedtime, to improve sleep quality");
    }

    // Support system
    if (formData.supportSystem == 0) {
        recommendations.push("🤝 Build social connections through community groups, therapy, or support networks");
    }

    // Symptoms-based recommendations
    if (formData.feelingNervous || formData.troubleConcentrating) {
        recommendations.push("🧘‍♀️ Practice mindfulness, deep breathing, or meditation for anxiety management");
    }

    if (formData.hopelessness || formData.stressfulMemories) {
        recommendations.push("💭 Consider professional counseling or therapy for emotional support");
    }

    // General recommendations
    recommendations.push("📚 Explore our mental health articles and resources");
    recommendations.push("👨‍⚕️ Connect with qualified mental health professionals in our directory");

    return recommendations;
}

async function submitAssessment(event) {
    event.preventDefault();

    // Show loading state
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = 'Processing with AI Model...';

    // Collect form data
    const formData = {
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        sleepHours: parseInt(document.getElementById('sleepHours').value),
        physicalActivity: parseInt(document.getElementById('physicalActivity').value),
        screenTime: parseInt(document.getElementById('screenTime').value),
        workHours: parseInt(document.getElementById('workHours').value),
        financialStress: parseInt(document.getElementById('financialStress').value),
        feelingNervous: document.getElementById('feelingNervous').checked,
        troubleConcentrating: document.getElementById('troubleConcentrating').checked,
        hopelessness: document.getElementById('hopelessness').checked,
        anger: document.getElementById('anger').checked,
        avoidsPeople: document.getElementById('avoidsPeople').checked,
        nightmares: document.getElementById('nightmares').checked,
        stressfulMemories: document.getElementById('stressfulMemories').checked,
        supportSystem: parseInt(document.getElementById('supportSystem').value),
        familyHistory: parseInt(document.getElementById('familyHistory').value),
        medicationUsage: parseInt(document.getElementById('medicationUsage').value)
    };

    try {
        // Send to API for ML model prediction
        const response = await fetch('/api/assessment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            const assessment = data.assessment;
            
            // Get risk level details
            const riskLevel = getRiskLevel(assessment.riskScore);
            
            // Store assessment results
            const assessmentResult = {
                ...formData,
                riskScore: assessment.riskScore,
                riskLevel: assessment.riskLevel,
                riskFactors: assessment.riskFactors,
                recommendations: assessment.recommendations,
                prediction: assessment.prediction,
                predictionProbability: assessment.predictionProbability,
                assessmentDate: new Date().toISOString(),
                mlModelUsed: true
            };

            localStorage.setItem('mentalHealthAssessment', JSON.stringify(assessmentResult));

            // Show results
            showResults(assessmentResult, riskLevel, assessment.predictionProbability);
        } else {
            alert('Error: ' + (data.error || 'Failed to process assessment'));
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    } catch (error) {
        console.error('Assessment error:', error);
        alert('An error occurred while processing your assessment. Please try again.');
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }
}

function showResults(assessment, riskLevel, predictionProbability = null) {
    const container = document.querySelector('.assessment-container');
    
    // Add ML model indicator if available
    const mlIndicator = assessment.mlModelUsed && predictionProbability !== null 
        ? `<div style="background: #e3f2fd; padding: 10px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #2196f3;">
            <strong>🤖 AI-Powered Assessment</strong>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #555;">
                This assessment was analyzed using our trained machine learning model. 
                Risk probability: ${(predictionProbability * 100).toFixed(1)}%
            </p>
        </div>`
        : '';
    
    container.innerHTML = `
        <div class="assessment-results">
            <h2>Assessment Results</h2>
            ${mlIndicator}
            
            <div class="risk-score-card" style="border-left: 5px solid ${riskLevel.color};">
                <h3>Risk Level: <span style="color: ${riskLevel.color};">${riskLevel.level}</span></h3>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${assessment.riskScore}%; background: ${riskLevel.color};"></div>
                </div>
                <p class="score-text">Risk Score: ${assessment.riskScore}/100</p>
                <p>${riskLevel.description}</p>
            </div>

            ${assessment.riskFactors && assessment.riskFactors.length > 0 ? `
                <div class="risk-factors">
                    <h3>Identified Risk Factors:</h3>
                    <ul>
                        ${assessment.riskFactors.map(factor => `<li>${factor}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}

            <div class="recommendations">
                <h3>Personalized Recommendations:</h3>
                <ul>
                    ${assessment.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>

            <div class="next-steps">
                <h3>Next Steps:</h3>
                <div class="action-buttons">
                    <a href="index.html" class="btn btn-primary">Explore Resources</a>
                    <a href="login.html" class="btn btn-secondary">Create Account</a>
                    ${assessment.riskScore >= 40 ? '<a href="index.html#doctors" class="btn btn-danger">Find Professional Help</a>' : ''}
                </div>
            </div>
        </div>
    `;
}

// Theme management
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

// Initialize slider values and theme on page load
document.addEventListener('DOMContentLoaded', () => {
    updateSliderValue('financialStress');
    loadTheme();
});