from flask import Flask, render_template, redirect, url_for
from flask_mail import Mail,  Message

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp@gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'ri******a@gmail.com',
    MAIL_PASSWORD = 'Ma*****fe'
)

mail = Mail(app)

@app.route('/send-mail/')
def send_mail():
    msg = mail.send_message(
        'Send Mail tutorial!',
        sender='ri******a@gmail.com',
        recipients=['ri*********07@msn.com'],
        body="Congratulations you've succeeded!"
    )
    return 'Mail sent'