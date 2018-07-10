from flask import Flask, render_template
app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def index():
    return render_template('login.html');

@app.route('/login')
def login():
    return render_template('login.html');
