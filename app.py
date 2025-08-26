from flask import Flask, render_template, request, jsonify, send_file, Response
import smtplib
import random
import string
import os
import tempfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_CONFIG
from youtube_downloader import YouTubeDownloader

# Initialize YouTube downloader
yt_downloader = YouTubeDownloader()

app = Flask(__name__)

# In-memory storage (you can replace with database later)
todos = [
    {"id": 1, "text": "Sample task 1", "completed": False, "priority": "medium"},
    {"id": 2, "text": "Sample completed task", "completed": True, "priority": "low"}
]
next_id = 3

# Store verification codes temporarily
verification_codes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/tasks')
def tasks():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/install')
def install():
    return render_template('install.html')

@app.route('/downloader')
def downloader():
    return render_template('downloader.html')

@app.route('/check-ytdlp')
def check_ytdlp():
    if yt_downloader.is_available():
        try:
            import yt_dlp
            return jsonify({'status': 'installed', 'version': yt_dlp.version.__version__})
        except:
            return jsonify({'status': 'installed', 'version': 'unknown'})
    else:
        return jsonify({'status': 'not_installed', 'message': 'yt-dlp not available'})

@app.route('/download-video', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    
    if not url or not ('youtube.com' in url or 'youtu.be' in url):
        return jsonify({'success': False, 'error': 'Invalid YouTube URL'})
    
    result = yt_downloader.get_video_info(url)
    return jsonify(result)

@app.route('/download-file', methods=['POST'])
def download_file():
    data = request.get_json()
    url = data.get('url')
    format_id = data.get('format_id')
    
    return yt_downloader.download_file(url, format_id)

@app.route('/send-code', methods=['POST'])
def send_verification_code():
    data = request.get_json()
    email = data.get('email')
    
    # Generate 6-digit verification code
    code = ''.join(random.choices(string.digits, k=6))
    verification_codes[email] = code
    
    # Send email with verification code
    try:
        send_email(email, code)
        return jsonify({'success': True, 'message': 'Verification code sent to your email'})
    except Exception as e:
        # Fallback to demo mode if email fails
        return jsonify({'success': True, 'demo_code': code, 'message': 'Demo mode: Email service unavailable'})

def send_email(to_email, verification_code):
    # Get email configuration
    smtp_server = EMAIL_CONFIG['smtp_server']
    smtp_port = EMAIL_CONFIG['smtp_port']
    sender_email = EMAIL_CONFIG['sender_email']
    sender_password = EMAIL_CONFIG['sender_password']
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "TaskFlow - Your Verification Code"
    
    # Email body
    body = f"""
    Hello!
    
    Your verification code for TaskFlow is: {verification_code}
    
    This code will expire in 10 minutes.
    
    If you didn't request this code, please ignore this email.
    
    Best regards,
    TaskFlow Team
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, to_email, text)
    server.quit()

@app.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    
    if email in verification_codes and verification_codes[email] == code:
        # Remove used code
        del verification_codes[email]
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Invalid verification code'})

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    global next_id
    data = request.get_json()
    new_todo = {
        "id": next_id,
        "text": data['text'],
        "completed": False,
        "priority": data.get('priority', 'medium')
    }
    todos.append(new_todo)
    next_id += 1
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = data.get('completed', todo['completed'])
            todo['text'] = data.get('text', todo['text'])
            todo['priority'] = data.get('priority', todo.get('priority', 'medium'))
            return jsonify(todo)
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return '', 204

if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)