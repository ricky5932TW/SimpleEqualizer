import os
import time

from flask import Flask, render_template, jsonify, request
import webbrowser

app = Flask(__name__)


# Main entry point
@app.route('/')
def index():
    return render_template('index.html')


# Full version of the page
@app.route('/full')
def full():
    return render_template('full.html')


# Limited version of the page
@app.route('/limited')
def limited():
    return render_template('limited.html')


@app.route('/initialize', methods=['POST'])
def initialize():
    standard = request.form['standard']
    lower_bound = request.form['lower_bound']
    filePATH = request.form['filePATH']


# Endpoint for updating the content
@app.route('/update', methods=['POST'])
def update_content():
    # Here you would implement the logic to update the content
    # For example, fetch the latest instruction or status
    # And generate or fetch new image paths
    return jsonify(instruction="New Instructions",
                   status="New Status",
                   pic1="path_to_new_pic1.jpg",
                   pic2="/static/temp_img/full.png")


if __name__ == '__main__':
    # Run the app and open the browser
    webbrowser.open('http://127.0.0.1:5000/')
    time.sleep(1)
    app.run(debug=True)
