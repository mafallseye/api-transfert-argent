

import email
from flask import Flask, request, url_for, render_template
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
APP = Flask(__name__)
# APP.config.from_pyfile('config.cfg')


APP.config['MAIL_SERVER'] = 'smtp.gmail.com'
APP.config['MAIL_PORT'] = 465
APP.config['MAIL_USERNAME'] = 'maguettefseye@gmail.com'

APP.config['MAIL_PASSWORD'] = 'qklhksqmkoxmurra'
APP.config['MAIL_USE_TLS'] = False
APP.config['MAIL_USE_SSL'] = True
mail = Mail(APP)
# s = URLSafeTimedSerializer('Thisisasecret!')


@APP.route('/')
def index():
    return render_template('home.html')


@APP.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        msg = request.form['message']
        message = Message(
            subject, sender='maguettefseye@gmail.com', recipients=[email])
        message.body = msg
        mail.send(message)
        success = 'message sent'
        return render_template('result.html', success=success)
    #     return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
    # email = request.form['email']
    # token = s.dumps(email, salt="confirm-email")
    # msg = Message('Confirm email', sender='maguettefseye@gmail.com',
    #               recipients=[email])
    # link = url_for('confirm_email', token=token, _external=True)
    # msg.body = 'Your link is {}'.format(link)
    # mail.send(msg)
    # return 'The email you entered is {}.The token is {}'.format(email, token)


# @APP.route('/confirm_email/<token>')
# def confirm_email(token):
#     try:
#         email = s.loads(token, salt='confirm-email', max_age=3600)

#     except SignatureExpired:
#         return 'The token is expired'
#     return 'This token works !'


if __name__ == '__main__':
    APP.run(debug=True)
