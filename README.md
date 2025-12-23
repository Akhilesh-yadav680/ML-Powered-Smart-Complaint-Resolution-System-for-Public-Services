🏙️ Smart Complaint & Service Resolution System with ML & Analytics

A modern web-based platform that allows citizens to submit location-based complaints and enables operators to manage, analyze, and resolve them efficiently using Machine Learning and interactive dashboards.

🚀 Project Overview

The Smart Complaint & Service Resolution System digitalizes traditional complaint-handling workflows. Citizens can securely register, submit detailed complaints with location information, and track progress in real time. Complaints are automatically categorized and prioritized using NLP and ML techniques, while operators monitor and resolve issues through a data-driven dashboard.

This system is suitable for municipal corporations, government grievance portals, smart city platforms, and service-based organizations.

✨ Key Features
👤 Citizen

Secure signup and login

Location-based complaint submission

Spam and meaningless complaint filtering

Automatic category & priority assignment

Real-time status tracking

Delete own complaints (before resolution)

🧑‍💼 Operator (Admin)

Centralized dashboard for all complaints

Update complaint status (Pending / In Progress / Resolved)

Delete complaints only after resolution

Interactive analytics with charts

Category, priority, and status-based insights

🧠 Machine Learning & NLP

Text preprocessing using NLP techniques

ML-based complaint categorization

Rule-based priority detection (High / Medium / Low)

Spam detection for invalid submissions

🛠️ Tech Stack

Language: Python 3.10

Backend: Flask

Frontend: HTML, CSS, Bootstrap

Database: SQLite

ORM: SQLAlchemy

Machine Learning: Scikit-learn

NLP: NLTK

Visualization: Chart.js

📂 Project Structure
smart-complaint-system/
│
├── app.py
├── auth.py
├── database.py
├── model/
│   └── complaint_model.pkl
├── templates/
│   ├── base.html
│   ├── base_admin.html
│   ├── login.html
│   ├── signup.html
│   ├── client_dashboard.html
│   └── operator_dashboard.html
├── static/
│   ├── css/
│   └── js/
├── requirements.txt
└── README.md

⚙️ How to Run the Project
# Clone the repository
git clone https://github.com/Akhilesh-yadav680/Smart-Complaint-Service-Resolution-System-with-ML-Analytics.git

# Navigate to project directory
cd smart-complaint-system

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py


Open in browser:
👉 http://127.0.0.1:5000

📊 Project Documentation 
   https://drive.google.com/file/d/1j_8modXRiI8HdC5Xr9-qI_kSc5q7I4t5/view
📎 Project Presentation:
👉 https://drive.google.com/file/d/1gXcBX0LJhFThkmoCLEuX9FvaHWrNzQKZ/view

🎯 Use Cases

Government grievance systems

Municipal complaint portals

Smart city initiatives

Public service management platforms

🔮 Future Enhancements

Password hashing & enhanced security

Email/SMS notifications

Geo-mapping of complaints

Cloud deployment

Advanced NLP models

👨‍🎓 Author

Akhilesh
B.Tech – Computer Science (Data Science)