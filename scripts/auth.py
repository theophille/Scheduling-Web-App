from flask import Blueprint, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms import validators
from flask_pymongo import MongoClient
from our_scheduler.scripts.session import Session
from operator import itemgetter
import uuid
import bcrypt

auth = Blueprint('auth', __name__)

class LogInForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('SignUp')

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LogInForm()
    return render_template('login.html', form_box_title="Log In", button="Login", form=form)

@auth.route('/register', methods=['GET', 'POST'])
def signup_page():
    form = SignUpForm()
    return render_template('signup.html', form_box_title="Create an Account", button="Sign Up", form=form)

@auth.route('/submit', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        connect = MongoClient('mongodb+srv://theophille:r0cCsJ9FVlnvYVZx@cluster0.43n5t8l.mongodb.net/?retryWrites=true&w=majority')
        db = connect['scheduler']
        collection = db['users']

        username = request.form.get('username')
        email = request.form.get('email')

        if collection.count_documents({'username': username}) == 0 and collection.count_documents({'email': email}) == 0:
            password = request.form.get('password')
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            post = {
                "_id": str(uuid.uuid1()),
                "username": username,
                "email": email,
                "password": hashed_password
            }

            collection.insert_one(post)

            collection = db['events-lists']

            post = {
                "_id": str(uuid.uuid1()),
                "username": username,
                "events": []
            }

            collection.insert_one(post)

            return 'Form submited'

        else:
            return redirect('/auth/register')

@auth.route('/logged', methods=['GET', 'POST'])
def logged():
    if request.method == 'POST':
        connect = MongoClient('mongodb+srv://theophille:r0cCsJ9FVlnvYVZx@cluster0.43n5t8l.mongodb.net/?retryWrites=true&w=majority')
        db = connect['scheduler']
        collection = db['users']

        username = request.form.get('username')
        password = request.form.get('password')
        result = collection.find_one({'username': username})

        if result != None:
            if bcrypt.checkpw(password.encode('utf-8'), result['password']):
                session = Session.getInstance()
                session.username = username

                collection = db['events-lists']
                result = collection.find_one({ 'username': username })
                result['events'] = sorted(result['events'], key=itemgetter('date'))
                session.events = result['events']

                return render_template('control.html', username=username, events=result['events'])
            else:
                return 'Fail'
        else:
            Session.getInstance().reset()
            return redirect('/auth/login')
    else:
        if Session.getInstance().username != None:
            return render_template('control.html', username=Session.getInstance().username, events=Session.getInstance().events)
        else:
            return 'Forbiden'