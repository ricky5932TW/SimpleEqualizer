import os
import signal
import sys
import time
import multiprocessing
from flask import Flask, render_template, jsonify, request
import webbrowser
from measurement import MeasurementService
from package.history import History
from runtime_state import (
    current_run_id,
    read_instruction,
    read_status,
    start_run,
    write_instruction,
    write_status,
)


app = Flask(__name__)


def finish_measurement(process):
    process.join()
    if process.exitcode == 0:
        write_status('Analysis complete')
    else:
        write_status('Analysis failed')


def parse_repeat_count(value):
    try:
        count = int(value)
    except (TypeError, ValueError):
        count = 1
    return max(1, min(count, 20))


@app.route('/')
def index():
    write_status('press start to begin')
    write_instruction(' ')
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


@app.route('/history')
def history():
    return render_template(
        'history.html',
        records=History.list_recent(limit=20),
        database_enabled=History.is_configured(),
        database_path=History.database_path(),
    )


@app.route('/measure', methods=['POST'])
def measure():
    standard = request.form['standard']
    lower_bound = request.form['lower_bound']
    filePATH = request.form['filePATH']
    optimize = request.form['optimize']
    repeat_count = parse_repeat_count(request.form.get('repeat_count', 1))

    start_run()
    t1 = multiprocessing.Process(target=MeasurementService.run_measurement,
                                 args=(standard, lower_bound, filePATH, optimize, repeat_count))
    t1.start()
    finish_measurement(t1)

    # print datatype

    return render_template('full.html', standard=standard, lower_bound=lower_bound, filePATH=filePATH,
                           optimize=optimize, repeat_count=repeat_count)


@app.route('/measure_limited', methods=['POST'])
def measure_limited():
    band_raw = request.form['band']
    band = band_raw.split()
    # turn string to int
    print(band, type(band))
    band = list(map(int, band))
    repeat_count = parse_repeat_count(request.form.get('repeat_count', 1))

    start_run()
    t2 = multiprocessing.Process(target=MeasurementService.run_measurement_limited, args=(band, repeat_count))
    t2.start()
    finish_measurement(t2)

    # print datatype

    return render_template('limited.html', band=band_raw, repeat_count=repeat_count)


@app.route('/white_noise_test', methods=['POST'])
def white_noise_test():
    repeat_count = parse_repeat_count(request.form.get('repeat_count', 1))
    start_run()
    t3 = multiprocessing.Process(target=MeasurementService.white_noise_test, args=(repeat_count,))
    t3.start()
    finish_measurement(t3)
    return render_template('white_noise_test.html', repeat_count=repeat_count)


@app.route('/img')
def image():
    return jsonify(
        full="/static/temp_img/full.png",
        spectrum="/static/temp_img/Spectrum.png",
        run_id=current_run_id(),
    )


@app.route('/img_limited')
def image_limited():
    return jsonify(full="/static/temp_img/Spectrum.png", run_id=current_run_id())


@app.route('/status')
def get_text():
    return jsonify({'status': read_status(), 'run_id': current_run_id()})


@app.route('/instruction')
def get_instruction():
    return jsonify({'instruction': read_instruction(), 'run_id': current_run_id()})


@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'
    sys.exit()


if __name__ == '__main__':
    write_status('press start to begin')
    write_instruction(' ')

    webbrowser.open('http://127.0.0.1:5000/')
    time.sleep(0.2)
    app.run(debug=True)
