from flask import Blueprint, request, jsonify,render_template,redirect,url_for,flash
from database import DatabaseManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user



auth_bp = Blueprint('auth', __name__)


db_manager = DatabaseManager("localhost", "root", "admin", "cabrental")
db_manager.connect()

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with db_manager.connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
        if user:
            stored_password = user[2] 
            if check_password_hash(stored_password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')


    return render_template("home.html")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':


        #get the data

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        #validate password
        if password != confirm_password:
            flash('Passwords don\'t match.', category='error')
        
        # Check if the username already exists in the database

        # Check if the username already exists in the database
        with db_manager.connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            existing_user = cursor.fetchone()

        if existing_user:
            return render_template("auth/sign_up.html", error="Username already exists")

        # If username doesn't exist, insert the new user into the database
        with db_manager.connection.cursor() as cursor:
            sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, email,password))
            db_manager.connection.commit()

        db_manager.close()  # Close the connection after use

        return redirect(url_for('auth.login'))
    
    return render_template("auth/sign_up.html")

