from flask import render_template,redirect
from . import main

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Pitch Point'
    return render_template('index.html', title = title)