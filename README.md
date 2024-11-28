# StrokeApp
**# App for the management of Stroke patient's personal information*
**# This is a simple but comprehensive web application built to manage stroke patients' personal information, medical history, and risk assessments. The app is made/designed for healthcare professionals to help them manage stroke patients and monitor stroke risk factors.*
# Features
**# •	User Authentication: Secure login and registration system with hashed passwords.*
**# •	Patient Database: View, add, edit, and delete patient records.
**# •	Stroke Risk Calculation: Automated stroke risk assessment based on health and lifestyle factors.
**# •	Data Import: Bulk uploads patient data from CSV files for quick database population.
**# •	Responsive Design: User-friendly interface accessible on multiple devices.
**# •	Data Security: Designed to ensure patient confidentiality and secure data handling.
# Technologies Used
**# •	Backend: Python (Flask)
**# •	Database: SQLite for user authentication and MongoDB for patient records
**# •	Frontend: HTML, CSS (with Bootstrap), Jinja2 templates
**# •	Data Handling: Pandas for data import and processing
**# •	Version Control: Git and GitHub
# Installations/Prerequisites
**# 1.	PyCharm (version 3.13)
**# 2.	MongoDB (local instance)
**# 3.	SQLite3
**# 4.	Git
# Steps
**# 1.	Clone the Repository: git clone https://github.com/ChisNwo/stroke-management-app.git
**# 2.	Create and Activate a Virtual Environment: python -m venv venv 
**# source venv/bin/activate  # For Windows: venv\Scripts\activate
**# 3.	Install Dependencies: pip install -r requirements.txt
**# 4.	Setup Databases: Initialize the SQLite database: python db_creation.py
**# o	Configure MongoDB connection settings in config.py.
**# 5.	Run the Application: flask run
**# 6.	Access the App: Open your browser and go to http://127.0.0.1:5000.
# Usage
# Adding Patients
**# •	Navigate to the Add Patient section to enter individual patient details.
**# •	Use the Import Dataset button to upload bulk data via a CSV file.
# Viewing Patient Records
**# •	Go to the Patient List to view all stored patient records sorted by most recent entries.
**# •	Click on a patient's name to view detailed information, including stroke risk assessment.
# Managing Users
**# •	Log in to access features. Users must register if they don’t have an account.
# File Structure
**# │stroke-management-app/
**# ├── app.py                          # Main Flask app file
**# ├── db_creation.py          # Database setup and initialization script
**# ├── templates/                  # HTML templates for the app
**# ├── static/                 	       # Static files (CSS)
**# ├── data/                           # Folder for CSV datasets
**# ├── db_creation.py         # MongoDB connection configuration
**# ├── load_csv_to_mongo.py  # Python dependencies
**# └── README.md                 # Project documentation
# Future Enhancements
**# •	Integration with machine learning models for advanced stroke risk prediction.
**# •	Export patient data to various formats (e.g., CSV, PDF).
**# •	Role-based user access (e.g., admin vs. medical staff).
**# •	Integration with electronic health record (EHR) systems.
# Contributing
**# Contributions are welcome! To contribute:
**# 1.	Fork the repository.
**# 2.	Create a new branch for your feature/bug fix.
**# 3.	Submit a pull request with a detailed explanation of your changes.
# License
**# See the LICENSE file for details.
# Acknowledgments
**# •	Inspired by healthcare applications for efficient patient management.
**# •	Stroke risk assessment logic based on recommendations from the American Stroke Association and CDC.
# Contact
**# For inquiries or collaboration opportunities, contact:
**# •	Name: ChisNwo
**# •	Email: 2411309@leedstrinity
**# •	GitHub: com7033-assignment-ChisNwo
