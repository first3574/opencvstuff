from flask import Flask, render_template, request
import subprocess
import findyellow
import time

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def calibrator():
    if request.method == 'POST':
        hl = request.form['hl']
        sl = request.form['sl']
        vl = request.form['vl']
        hh = request.form['hh']
        sh = request.form['sh']
        vh = request.form['vh']
        findyellow.save_color_values(hl, sl, vl, hh, sh, vh)

    subprocess.call(['python', 'findyellow.py'])
    lowvals, highvals = findyellow.read_color_values()

    return render_template('calibration_template.html',
                           hl=lowvals[0],
                           sl=lowvals[1],
                           vl=lowvals[2],
                           hh=highvals[0],
                           sh=highvals[1],
                           vh=highvals[2],
                           blah=time.clock())


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
