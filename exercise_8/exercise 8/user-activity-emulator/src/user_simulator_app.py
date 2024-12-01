import pandas as pd
import requests
from user_simulator import UserSimulator
from flask import Flask, render_template, request

app = Flask(__name__)

recommender_endpoint = 'http://recommender-model:5000/recommender'
feedback_endpoint = 'http://feedback-collector:5000/feedback'
simulator = UserSimulator('data/user_activity.bz2', recommender_endpoint, feedback_endpoint)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle when the Start button is pushed
        if request.form['mybutton'] == 'Start':
            if not simulator.running:
                simulator.start()
                print("Simulator started", flush=True)
            else:
                print("Simulator is already running", flush=True)
        # Handle when the Stop button is pushed
        elif request.form['mybutton'] == 'Stop':
            if simulator.running:
                simulator.stop()
                print("Simulator stopped", flush=True)
            else:
                print("Simulator is not running", flush=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
