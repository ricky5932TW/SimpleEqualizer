import os
import signal
import sys
import time
import threading
import multiprocessing
from flask import Flask, render_template, jsonify, request, send_from_directory
import webbrowser
from measurement import Measurement_mission


def write_txt(data, filename='static/status.txt'):
    with open(filename, 'w') as f:
        f.write(data)


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


@app.route('/measure', methods=['POST'])
def measure():
    standard = request.form['standard']
    lower_bound = request.form['lower_bound']
    filePATH = request.form['filePATH']
    optimize = request.form['optimize']

    t1 = threading.Thread(target=Measurement_mission.Measurement, args=(standard, lower_bound, filePATH, optimize))
    t1.start()

    print(standard, type(standard))
    print(lower_bound, type(lower_bound))
    print(filePATH, type(filePATH))
    print(optimize, type(optimize))

    # print datatype

    return render_template('full.html', standard=standard, lower_bound=lower_bound, filePATH=filePATH,
                           optimize=optimize)


@app.route('/measure_limited', methods=['POST'])
def measure_limited():
    band_raw = request.form['band']
    band = band_raw.split()
    # turn string to int
    band = list(map(int, band))

    t1 = threading.Thread(target=Measurement_mission.Measurement_limited, args=band)
    t1.start()

    # print datatype

    return render_template('limited.html', band=band)


@app.route('/img')
def image():
    return jsonify(full="/static/temp_img/full.png", spectrum="/static/temp_img/Spectrum.png")


@app.route('/status')
def get_text():
    with open('static/status.txt', 'r') as f:
        status_ = f.read()
    return jsonify({'status': status_})


@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'
    sys.exit()


if __name__ == '__main__':
    write_txt('press start to begin')
    webbrowser.open('http://127.0.0.1:5000/')
    time.sleep(0.5)
    app.run(debug=True)
