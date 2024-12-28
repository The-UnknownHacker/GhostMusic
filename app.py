import os
import glob
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from io import BytesIO
import requests
import ffmpeg
import numpy as np

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)

with app.app_context():
    db.create_all()
    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'error'

print(f'Current API Key: {os.getenv("HF_API_KEY")}')

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"API Error: Status {response.status_code}")
            print(f"API Response: {response.text}")
            return None
        return response.content
    except Exception as e:
        print(f"Query error: {str(e)}")
        return None

def convert_audio_to_numpy(audio_bytes, sample_rate):
    out, _ = (
        ffmpeg
        .input('pipe:0')
        .output('pipe:1', format='wav', acodec='pcm_s16le', ar=str(sample_rate))
        .run(input=audio_bytes, capture_stdout=True, capture_stderr=True)
    )
    audio_data = np.frombuffer(out, dtype=np.int16)
    return audio_data

def audio_write(file_name, audio_data, sample_rate):
    if not file_name.endswith('.wav'):
        file_name += '.wav'
    input_stream = BytesIO(audio_data)
    ffmpeg.input('pipe:0').output(file_name, format='wav', acodec='pcm_s16le', ar=str(sample_rate)).run(input=input_stream.read())
    print(f"Audio saved as {file_name}")

@app.route('/')
@login_required
def index():
    color_scheme = session.get('color_scheme', 'light')
    return render_template('index.html', username=current_user.id if current_user.is_authenticated else None, color_scheme=color_scheme)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/change_theme', methods=['POST'])
def change_theme():
    color_scheme = request.form.get('color_scheme')
    session['color_scheme'] = color_scheme
    return redirect(url_for('index'))

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    try:
        if request.method == 'POST':
            data = request.get_json()
            prompt = data.get('prompt')
            if not prompt:
                return "Prompt is required", 400

            print(f"Received prompt: {prompt}")

            audio_bytes = query({
                "inputs": prompt,
            })

            if not audio_bytes:
                return "Failed to generate audio bytes", 400

            output_dir = "static/audio"
            existing_files = glob.glob(f"{output_dir}/output*.wav")
            next_number = len(existing_files) + 1
            filename = f"output{next_number}"

            sample_rate = 22050
            audio_data = convert_audio_to_numpy(audio_bytes, sample_rate)

            audio_write(f"{output_dir}/{filename}", audio_bytes, sample_rate)

            return {
                'audio_url': url_for('download_audio', filename=f"{filename}.wav")
            }
    except Exception as e:
        print(f"Error in generate_audio: {str(e)}")
        return f"Error: {str(e)}", 400

@app.route('/download_audio/<filename>')
@login_required
def download_audio(filename):
    audio_dir = os.path.join(os.getcwd(), 'static', 'audio')
    return send_from_directory(audio_dir, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
