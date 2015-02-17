from flask import Flask, render_template, request
import findyellow
import cv2

app = Flask(__name__)

@app.route('/')
def calibrator():
    if request.method == 'POST':
        hl = request.form['hl']
        sl = request.form['sl']
        vl = request.form['vl']
        hh = request.form['hh']
        sh = request.form['sh']
        vh = request.form['vh']
    cap = cv2.VideoCapture(1)
    lowvals, highvals = findyellow.read_color_values()
    mask = findyellow.get_yellow_frame(cap, lowvals, highvals)
    cv2.imwrite("static/tempcalibrate.png", mask );
    return render_template('calibration_template.html',
                           hl=lowvals[0],
                           sl=lowvals[1],
                           vl=lowvals[2],
                           hh=highvals[0],
                           sh=highvals[1],
                           vh=highvals[2])

if __name__ == '__main__':
    app.run(debug=True)