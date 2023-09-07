from flask import Flask, request, render_template, session, redirect, url_for, flash
import hashlib
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import bcrypt
from user import User
import os
from database import Database  # Import your Database class
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
import pandas as pd

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Initialize your Flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOADED_DATA_DEST'] = 'uploads'
data_files = UploadSet('data', DOCUMENTS)
configure_uploads(app, data_files)


# Create an instance of the Database class
db = Database()
db.checkConnection() #Check connection to database
user = User()


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check user credentials
        if user.checkIfUserExists(username):
            stored_password = user.getUserPassword(username)
            
            if bcrypt.checkpw(password.encode('utf-8',), stored_password):
                session['username'] = username
                return redirect (url_for('dashboard'))
          
        return render_template('login.html', error=True)  
    
    return render_template('login.html', error=False)
 

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    userAlreadyExists = False
    passwordMismatch = False  # Add a flag for password mismatch
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeated_password = request.form['repeat_password']
        
        # Check if the username already exists in the database
        if user.checkIfUserExists(username):
            userAlreadyExists = True
        # Check if the passwords match
        elif password != repeated_password:
            passwordMismatch = True
        else:
            # Hash the password before storing it in the database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            print(hashed_password)

            # Insert the new user into the database
            user.createNewUser(username, hashed_password)

            # Redirect the user to the login page after successful signup
            return redirect(url_for('login'))

    return render_template('signup.html', error_user_exists=userAlreadyExists, error_password_mismatch=passwordMismatch)

# Dashboard route (requires login)
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        if request.method == 'POST' and 'data_file' in request.files:
            data_file = request.files['data_file']
            if data_file.filename != '':
            # Check the file extension
                if data_file.filename.endswith(('.xls', '.xlsx')):
                    # Save the uploaded file
                    filename = data_files.save(data_file)

                    # Load the Excel file into a DataFrame
                    file_path = os.path.join('uploads', filename)
                    df = pd.read_excel(file_path)

                    # Display the data in the template
                    return render_template('dashboard.html', data=df.to_html(classes='table table-striped table-bordered'))
                else:
                    flash('Invalid file format. Please upload an Excel file.')
            else:
                flash('No file selected for upload.')

        return render_template('dashboard.html', data=None)
    else:
        return redirect(url_for('login'))



# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
