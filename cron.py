from pymongo import MongoClient
from datetime import date, datetime
import smtplib

connect = MongoClient('mongodb+srv://theophille:r0cCsJ9FVlnvYVZx@cluster0.43n5t8l.mongodb.net/?retryWrites=true&w=majority')
db = connect['scheduler']
collection = db['events-lists']

lists = collection.find({})
collection = db['users']

sender = 'at.proiect.iap4@gmail.com'
password = 'wtanegntkxtysgkf'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)
print('Logged in to server')

for list in lists:
    index = 0
    delete_indexes = []
    for event in list['events']:
        index += 1
        ev_date = datetime.strptime(event['date'], '%Y-%m-%d')
        today = str(date.today())
        td_date = datetime.strptime(today, '%Y-%m-%d')
        delta = ev_date - td_date
        if delta.days <= 1 and delta.days >= 0:
            collection = db['users']
            user = collection.find_one({ 'username': list['username'] })
            recv = user['email']
            time = datetime.strptime(event['start'], '%H:%M')
            message = event['name'] + ' is coming. It starts tomorrow at ' + str(time.hour) + '.' + str(time.minute) + '.'
            server.sendmail(sender, recv, message)
            print(message)
            collection = db['events-lists']

        elif delta.days < 0:
            print('removal')
            list['events'].remove(event)
    
    newvalues = { "$set": { 'events': list['events']} }
    collection.update_one({ 'username': list['username']}, newvalues)