import os
import signal
import sys
import time
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
    write_txt('press start to begin')
    write_txt(filename='instruction.txt', data=' ')
    return render_template('index.html')


@app.route('/full')
def full():
    return render_template('full.html')


@app.route('/limited')
def limited():
    return render_template('limited.html')


@app.route('/white_noise')
def white_noise():
    return render_template('white_noise_test.html')


@app.route('/measure', methods=['POST'])
def measure():
    standard = request.form['standard']
    lower_bound = request.form['lower_bound']
    filePATH = request.form['filePATH']
    optimize = request.form['optimize']

    write_txt('Analyzing ...')
    t1 = multiprocessing.Process(target=Measurement_mission.Measurement,
                                 args=(standard, lower_bound, filePATH, optimize))
    t1.start()
    t1.join()
    write_txt('Analysis complete')

    # print datatype

    return render_template('full.html', standard=standard, lower_bound=lower_bound, filePATH=filePATH,
                           optimize=optimize)


@app.route('/measure_limited', methods=['POST'])
def measure_limited():
    band_raw = request.form['band']
    band = band_raw.split()
    # turn string to int
    print(band, type(band))
    band = list(map(int, band))

    t2 = multiprocessing.Process(target=Measurement_mission.Measurement_limited, args=(band,))
    t2.start()
    t2.join()
    write_txt('Analysis complete')

    # print datatype

    return render_template('limited.html', band=band_raw)


@app.route('/white_noise_test', methods=['POST'])
def white_noise_test():
    t3 = multiprocessing.Process(target=Measurement_mission.white_noise_test)
    t3.start()
    t3.join()
    write_txt('Analysis complete')
    return render_template('white_noise_test.html')


@app.route('/img')
def image():
    return jsonify(full="/static/temp_img/full.png", spectrum="/static/temp_img/Spectrum.png")


@app.route('/img_limited')
def image_limited():
    return jsonify(full="/static/temp_img/Spectrum.png")


@app.route('/status')
def get_text():
    with open('static/status.txt', 'r') as f:
        status_ = f.read()
    return jsonify({'status': status_})


@app.route('/instruction')
def get_instruction():
    with open('instruction.txt', 'r') as f:
        instruction_ = f.read()
    return jsonify({'instruction': instruction_})


@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'
    sys.exit()


if __name__ == '__main__':
    write_txt('press start to begin')
    write_txt(filename='instruction.txt', data=' ')
    # remove old temp_img
    try:
        os.remove('static/temp_img/full.png')
    except:
        pass
    try:
        os.remove('static/temp_img/Spectrum.png')
    except:
        pass
    try:
        os.remove('static/temp_img/separated_spectrum.png')
    except:
        pass

    webbrowser.open('http://127.0.0.1:5000/')
    time.sleep(0.2)
    app.run(debug=True)
