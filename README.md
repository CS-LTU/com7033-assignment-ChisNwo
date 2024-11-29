# StrokeApp
<<<<<<< HEAD
This is a simple but comprehensive web application built to manage stroke patients' personal information, medical history, and risk assessments.
The app is made/designed for healthcare professionals to help them manage stroke patients and monitor stroke risk factors.
# Features
* User Authentication: Secure login and registration system with hashed passwords.
* Patient Database: View, add, edit, and delete patient records.
* Stroke Risk calculation: Automated stroke risk assessment based on health and lifestyle factors.
* Data import: Bulk upload of patient data from CSV files for quick database population.
* Responsive design: User friendly interface accessible on multiple devices
* Data Security: Designed to ensure patients confidentiality and secure data handling

# Installations
1. Pycharm (version 3.8)
2. MongoDB
3. SQLite3
4. Git
=======
# Steps
1. Clone the repository: git clone http://github.com/ChisNwo/stroke_management-app.git
2. Create and activate a Virtual Environment: python -m venu venu soource venu/bin/activate
3. Install dependencies: pip install -r requirements.txt
4. Setup database: Initialise the SQLite database: python db_creation.py
     Configure MongoDB connection settings in mongo_setup.py
5. Run the application': flask run
6. Access the App: Open your browser and go to http://127.0.0.1:5000.

# Application
> project_root/
├── strokesHospitalApp/
│   ├── app.py                # Application file
│   ├── db_creation.py        # Database configurations
│   ├── db_function.py        # Database operation functions   
│   ├── tests.py              # Test suite for the application  
│   ├──load_csv_to_mongo.py   # Importing C|SV file into mongo.py
│   ├──mongo_setup.py         # Mongodb set up
│   ├── static/                # Static files (CSS)
│   │   ├── main.css           # CSS stylesheets
│   ├── templates/             # HTML templates
│   │   ├── add_patient.html
│   │   ├── delete_patient.html
│   │   ├── home_page.html main_layout.html
│   │   ├── edit_patient.html
│   │   ├── edit_user.html
│   │   ├── error.html
│   │   ├── login.html
│   │   ├── main_layout.html
│   │   ├── patient.html
│   │   ├── register_page.html
│   │   ├── patient_information.html
│   ├── dataset.csv             # CSV file with patient data
│   ├──user_base.db             # User registration db
│   └── requirements.txt        # List of libraries installed
└── README.md                   # README file

# Testing the App
Test the Flask application by running:
test.py
Test includes: Homepage, login, registration pages
User authentication and database operations verification.

# Contributing
Contributions are welcome. To do so;
1. Fork the repository
2. Create a new branch for your feature/bug fix
3. Submit a pull request with a detailed explanation of your changes.

# The Technologies used for this App
Backend: Pycharm (Python Flask)
Microsoft Office
Notepad++
Databases: MongoDB Compass for patient records and SQLite for user authentication
Frontend: HTML, CSS (with Bootstrap), Jinja2 templates
Version Control: Git and GitHub

# AI Used
AI tools like ChatGPT was used in this project. It was used during the development phase for planning, brainstorming, and editing. 
* This statement is being added to ensure compliance with academic requirements.

# Future Enhancements
* Integration with machine learning models for advanced stroke risk prediction
* Export patient data to various formats (e.g., CSV, PDF)
* Role based user access (e.g Admin)
* Integration with electronic health record (EHR) systems.

# Licences
See the Licence file for details

# Author
ChisNwo
Leeds Trinity University
Version 1.0