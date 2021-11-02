from flask import render_template
from flask_mail import Message
from . import mail
import string
import random

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)

def send_password_reset_email(email, password):
    send_email('[FIND MY HDB] Reset Your Password',
               sender='noreply@test2006.com',
               recipients=[email],
               text_body=render_template('reset_password.txt', password = password))

def generate_password():
    password= ""
    
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()<>/?") 
    random.shuffle(characters)

    pwLength = random.randint(8,15)

    for i in range (pwLength):
        password += random.choice(characters)

    return str(password)
