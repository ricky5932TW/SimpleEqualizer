import os
import time
import threading
from flask import Flask, render_template, jsonify, request, send_from_directory
import webbrowser

app = Flask(__name__)

status = {"status": "press start to begin"}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/full')
def full():
    return render_template('full.html')


@app.route('/limited')
def limited():
    return render_template('limited.html')


@app.route('/initialize', methods=['POST'])
def initialize():
    standard = request.form['standard']
    lower_bound = request.form['lower_bound']
    filePATH = request.form['filePATH']
    meausre_thread = threading.Thread(target=meausre, args=(standard, lower_bound, filePATH))

    print(standard, lower_bound, filePATH)
    return render_template('full.html', standard=standard, lower_bound=lower_bound, filePATH=filePATH)

@app.route('/img')
def image():
    return jsonify(full="/static/temp_img/full.png", spectrum="/static/temp_img/Spectrum.png")

@app.route('/status')
def get_text():
    return jsonify(status)


# Endpoint for updating the content
@app.route('/update', methods=['POST'])
def update_content():
    # Here you would implement the logic to update the content
    # For example, fetch the latest instruction or status.txt
    # And generate or fetch new image paths
    return jsonify(instruction="New Instructions",
                   status="New Status",
                   pic1="path_to_new_pic1.jpg",
                   pic2="/static/temp_img/full.png")


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    time.sleep(1)
    app.run(debug=True)
