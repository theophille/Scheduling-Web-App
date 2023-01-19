from flask import Blueprint, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField
from wtforms import validators
from flask_pymongo import MongoClient
from our_scheduler.scripts.session import Session
from operator import itemgetter

scd = Blueprint('scd', __name__)

class AddForm(FlaskForm):
    name = StringField('Event', [validators.DataRequired()])
    date = DateField('Date', [validators.DataRequired()])
    start = TimeField('Event starts at:', [validators.DataRequired()])
    end = TimeField('Event ends at:', [validators.DataRequired()])
    submit = SubmitField('Add event')

class RemoveForm(FlaskForm):
    name = StringField('Event', [validators.DataRequired()])
    submit = SubmitField('Remove Event')


@scd.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    return render_template('add-event.html', form=form)

@scd.route('/add/validate', methods=['GET', 'POST'])
def add_validate():
    if request.method == 'POST':
        connect = MongoClient('mongodb+srv://theophille:r0cCsJ9FVlnvYVZx@cluster0.43n5t8l.mongodb.net/?retryWrites=true&w=majority')
        db = connect['scheduler']
        collection = db['events-lists']

        username = Session.getInstance().username
        print(username)
        result = collection.find_one({'username': username})

        if result != None:
            event = {
                'name': request.form.get('name'),
                'date': request.form.get('date'),
                'start': request.form.get('start'),
                'end': request.form.get('end')
            }

            print(event)

            Session.getInstance().events.append(event)
            Session.getInstance().events = sorted(Session.getInstance().events, key=itemgetter('date'))

            newvalues = { "$set": { 'events': Session.getInstance().events} }

            collection.update_one({ 'username': username }, newvalues)
        else:
            print("Not working")

    return redirect('/auth/logged')

@scd.route('/remove', methods=['GET', 'POST'])
def remove():
    form = RemoveForm()
    return render_template('remove-event.html', form=form, username=Session.getInstance().username)

@scd.route('/remove/validate', methods=['GET', 'POST'])
def remove_validate():
    if request.method == 'POST':
        connect = MongoClient('mongodb+srv://theophille:r0cCsJ9FVlnvYVZx@cluster0.43n5t8l.mongodb.net/?retryWrites=true&w=majority')
        db = connect['scheduler']
        collection = db['events-lists']

        username = Session.getInstance().username

        result = collection.find_one({'username': username})

        if result != None:

            for event in result['events']:
                if event['name'] == request.form.get('name'):
                    Session.getInstance().events.remove(event)

            newvalues = { "$set": { 'events': Session.getInstance().events} }
            collection.update_one({ 'username': username }, newvalues)

        else:
            print("Not working")

    return redirect('/auth/logged')