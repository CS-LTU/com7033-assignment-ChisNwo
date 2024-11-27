from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from functools import wraps
import pandas as pd
from db_creation import get_db_connection, get_mongodb_connection, init_databases

# start databased
init_databases()

# connection with mongoDB
mongo_db = get_mongodb_connection()
patients = mongo_db.patients

# # I need this to keep user sessions secure
app = Flask(__name__)
app.secret_key = os.urandom(24)


# This is my security check - it makes sure nobody can register twice
# App check both username and email
def user_exists(username, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ? AND email = ?", (username, email))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None


# This decorator is really useful as it checks if a user is logged in before displaying any pages,
# and redirects them to the login page if they are not logged in.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Routes to the home page
@app.route('/')
def home_page():
    return render_template('home_page.html')


# Page where users log in
# App check if their email exists and if their password is correct
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Logged in successfully!')
            return redirect(url_for('home_page'))
        flash('Invalid email or password')
    return render_template('login.html')


# users create new account
# App checks if email already exists and hash their password before saving it
@app.route('/register_page', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                         (name, email, password))
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!')
        finally:
            conn.close()
    return render_template('register_page.html')


# page with all patients
# Sorted by newest
@app.route('/patients_list')
@login_required
def patients_list():
    # id sorted, new added on the top list
    patient_list = list(patients.find().sort('_id', -1))
    return render_template('patient_information.html', patients=patient_list)


# load list of patients from folder
# users can easily import their data
#
# App check all the data that comes from CSV:
# Make sure all text values are correct
# Check if numbers make sense (like age can't be 200)
# Fix or replace any wrong values
#
# App also made it safe:
# Check if file exists and isn't empty
# Don't add the same patient twice
# If one patient has bad data, others can still be added
#
# This helps keep my database clean and my risk calculations accurate
def import_dataset_data():
    try:
        # path to csv file
        csv_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')

        # read CSV
        df = pd.read_csv(csv_path)

        # count added patients
        added_count = 0

        # check each row from CSV
        for _, row in df.iterrows():
            try:
                # Check and fix all data before adding to patient_data:

                # Check gender - must be "Male" or "Female"
                gender = str(row['gender']) if pd.notna(row['gender']) else "Unknown"
                if gender not in ["Male", "Female"]:
                    gender = "Unknown"

                # Check age
                age = float(row['age']) if pd.notna(row['age']) else 0.0
                if age < 0 or age > 120:
                    age = 0.0

                # Check hypertension - must be 0 or 1
                hypertension = int(row['hypertension']) if pd.notna(row['hypertension']) else 0
                if hypertension not in [0, 1]:
                    hypertension = 0

                # Check marriage status
                ever_married = str(row['ever_married']) if pd.notna(row['ever_married']) else "Unknown"
                if ever_married not in ["Yes", "No"]:
                    ever_married = "Unknown"

                # Check work type
                work_type = str(row['work_type']) if pd.notna(row['work_type']) else "Unknown"
                if work_type not in ["Private", "Self-employed", "Govt_job", "children", "Never_worked"]:
                    work_type = "Unknown"

                # Check residence type
                residence_type = str(row['Residence_type']) if pd.notna(row['Residence_type']) else "Unknown"
                if residence_type not in ["Urban", "Rural"]:
                    residence_type = "Unknown"

                # Check glucose - must be realistic medical value
                glucose = float(row['avg_glucose_level']) if pd.notna(row['avg_glucose_level']) else 0.0
                if glucose < 0 or glucose > 500:  # normal values are between 0 and 500
                    glucose = 0.0

                # BMI check
                bmi = float(row['bmi']) if pd.notna(row['bmi']) else 0.0
                if bmi < 10:
                    bmi = 25.0

                # Check smoking status
                smoking = str(row['smoking_status']) if pd.notna(row['smoking_status']) else "Unknown"
                if smoking not in ["never smoked", "formerly smoked", "smokes", "Unknown"]:
                    smoking = "Unknown"

                # Create patient data with all checked values
                patient_data = {
                    'gender': gender,
                    'age': age,
                    'hypertension': hypertension,
                    'ever_married': ever_married,
                    'work_type': work_type,
                    'residence_type': residence_type,
                    'avg_glucose_level': glucose,
                    'bmi': bmi,
                    'smoking_status': smoking
                }

                # Calculate risk factors
                risk_factors = 0
                if patient_data['hypertension'] == 1:
                    risk_factors += 0.3
                if patient_data['age'] > 60:
                    risk_factors += 0.3
                if patient_data['avg_glucose_level'] > 200:
                    risk_factors += 0.2
                if patient_data['smoking_status'] == 'smokes':
                    risk_factors += 0.2

                patient_data['stroke_risk'] = min(risk_factors, 1.0)

                # Check if patient already exists
                existing_patient = patients.find_one({
                    'gender': patient_data['gender'],
                    'age': patient_data['age'],
                    'hypertension': patient_data['hypertension'],
                    'avg_glucose_level': patient_data['avg_glucose_level']
                })

                # Add new patients only
                if not existing_patient:
                    patients.insert_one(patient_data)
                    added_count += 1

            except Exception as e:
                print(f"Error processing record: {str(e)}")
                continue

        return True, f"Successfully imported {added_count} new patient records"

    except FileNotFoundError:
        return False, "No file"
    except pd.errors.EmptyDataError:
        return False, "Empty data"
    except Exception as e:
        return False, f"Error data: {str(e)}"


# This is the button that uses my import function. If something goes wrong, app show an error message
@app.route('/import_dataset', methods=['GET'])
@login_required
def import_dataset_route():
    success, message = import_dataset_data()
    if success:
        flash(message)
    else:
        flash(message, 'error')
    return redirect(url_for('patients_list'))


# # This is where app add new patients and check their stroke risk
# I got these risk values from the American Stroke Association and CDC resources:
# High blood pressure adds 0.3 to risk
# Being over 60 adds 0.3
# High glucose adds 0.2
# Smoking adds 0.2
# The most someone can get is 1.0 (100% risk)

@app.route('/add_patients', methods=['GET', 'POST'])
@login_required
def add_patients_route():
    if request.method == 'POST':
        patient_data = {
            'gender': request.form['gender'],
            'age': float(request.form['age']),
            'hypertension': int(request.form['hypertension']),
            'ever_married': request.form['ever_married'],
            'work_type': request.form['work_type'],
            'residence_type': request.form['residence_type'],
            'avg_glucose_level': float(request.form['avg_glucose_level']),
            'bmi': float(request.form['bmi']),
            'smoking_status': request.form['smoking_status']
        }
        risk_factors = 0.0
        if patient_data['hypertension'] == 1:
            risk_factors += 0.3
        if patient_data['age'] > 60:
            risk_factors += 0.3
        if patient_data['avg_glucose_level'] > 200:
            risk_factors += 0.2
        if patient_data['smoking_status'].lower() == 'smokes':
            risk_factors += 0.2

        stroke_risk = float(min(risk_factors, 1.0))
        patient_data['stroke_risk'] = stroke_risk

        patients.insert_one(patient_data)

        flash('Patient added successfully!')
        return render_template('patient.html',
                               stroke_risk=stroke_risk,
                               hypertension=patient_data['hypertension'],
                               age=patient_data['age'],
                               glucose=patient_data['avg_glucose_level'],
                               smoking=patient_data['smoking_status'])

    return redirect(url_for('patients_list'))


# When someone clicks on a patient info button, this shows all their details

@app.route('/patient_information/<string:patient_id>')
@login_required
def patient_information(patient_id):
    patient = patients.find_one({'_id': ObjectId(patient_id)})
    if patient:
        return render_template('patient_information.html', patient=patient)
    flash('Patient not found!')
    return redirect(url_for('patients_list'))


# This is how users log out. I use session.clear() to remove all their data
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('home_page'))


@app.route('/edit_patient/<string:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    patient = patients.find_one({'_id': ObjectId(patient_id)})
    if not patient:
        flash('Patient not found!')
        return redirect(url_for('patients_list'))

    if request.method == 'POST':
        try:
            # Download and change data from dataset
            updated_data = {
                'gender': request.form['gender'],
                'age': float(request.form['age']),
                'hypertension': int(request.form['hypertension']),
                'ever_married': request.form['ever_married'],
                'work_type': request.form['work_type'],
                'residence_type': request.form['residence_type'],
                'avg_glucose_level': float(request.form['avg_glucose_level']),
                'bmi': float(request.form['bmi']),
                'smoking_status': request.form['smoking_status']
            }

            # Risk Factor Calculator
            risk_factors = 0.0
            if updated_data['hypertension'] == 1:
                risk_factors += 0.3
            if updated_data['age'] > 60:
                risk_factors += 0.3
            if updated_data['avg_glucose_level'] > 200:
                risk_factors += 0.2
            if updated_data['smoking_status'].lower() == 'smokes':
                risk_factors += 0.2

            updated_data['stroke_risk'] = min(risk_factors, 1.0)

            # Update Patient infi in database
            result = patients.update_one(
                {'_id': ObjectId(patient_id)},
                {'$set': updated_data}
            )

            if result.modified_count > 0:
                flash('Patient updated successfully!')
            else:
                flash('No changes were made.')

            return redirect(url_for('patients_list'))

        except ValueError as e:
            flash('Invalid data format. Please check your inputs.')
        except Exception as e:
            flash(f'Error updating patient: {str(e)}')

    return render_template('edit_patient.html', patient=patient)


@app.route('/delete_patient/<string:patient_id>')
@login_required
def delete_patient(patient_id):
    patients.delete_one({'_id': ObjectId(patient_id)})
    flash('Patient deleted successfully!')
    return redirect(url_for('patients_list'))


@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    conn = get_db_connection()
    if request.method == 'POST':
        # User data update
        name = request.form['name']
        email = request.form['email']
        conn.execute('UPDATE users SET name = ?, email = ? WHERE id = ?',
                     (name, email, session['user_id']))
        conn.commit()
        flash('User information updated successfully!')
        return redirect(url_for('home_page'))
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('edit_user.html', user=user)


@app.route('/delete_user')
@login_required
def delete_user():
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (session['user_id'],))
    conn.commit()
    conn.close()
    session.clear()
    flash('Your account has been deleted.')
    return redirect(url_for('home_page'))


# This runs my app; (debug=True) - shows me errors when something goes wrong
if __name__ == '__main__':
    app.run(debug=True)