from our_scheduler import app
from flask import render_template, redirect

@app.route('/')
def hello():
    return redirect('/auth/login')

from our_scheduler.scripts.auth import *
from our_scheduler.scripts.scheduler import *