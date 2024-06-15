from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    receiver_email = data.get('receiver_email')
    subject = data.get('subject')
    body_text = data.get('body_text')

    if not receiver_email or not subject or not body_text:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[receiver_email])
        msg.body = body_text
        mail.send(msg)
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:  
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
