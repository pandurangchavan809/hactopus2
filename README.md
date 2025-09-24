# 🟢 Hactopus – Online Dispute Resolution Platform

## 📌 Overview
**Hactopus** is an AI-powered Online Dispute Resolution (ODR) web platform that helps individuals, businesses, and consumers **file disputes, upload evidence, and receive smart settlement suggestions**.  
Our goal is to make conflict resolution **faster, transparent, and accessible**.

---

## ✨ Key Features
- **📝 Complaint Management**: File and track disputes with detailed descriptions and evidence.
- **🤖 AI Assistance**: Gemini API–driven suggestions for possible resolutions and next steps.
- **📂 Evidence Storage**: Securely upload images, PDFs, or videos as supporting documents.
- **👤 Google Authentication**: Quick sign-in with Google using Firebase Auth.
- **📊 User Dashboard**: View complaint status, history, and consumer rights information.
- **🔒 Secure Cloud Backend**: Firestore & Firebase Storage ensure data safety and scalability.

---

## 🏗️ Tech Stack
| Layer          | Technology                        |
|----------------|------------------------------------|
| **Frontend**   | HTML5, CSS3, JavaScript (Vanilla) |
| **Backend**    | Python **Flask** REST API         |
| **Database**   | **Firebase Firestore** (NoSQL)    |
| **Auth**       | Firebase Authentication (Google)  |
| **File Storage**| Firebase Cloud Storage           |
| **AI/ML**      | Google **Gemini API** for NLP     |
| **Hosting**    | Firebase Hosting or Render/Heroku for Flask backend |

---

## 🗂️ Project Structure
hactopus/
├── frontend/ # UI files
│ └── index.html and other files
├── backend/ # Flask application
│ ├── app.py # Flask API endpoints
│ └── serviceAccountKey.json # Firebase Admin credentials (not committed)
├── requirements.txt
└── README.md