from flask import Flask, render_template, request, jsonify
from colored_printing import *
from stepper_motor import StepperMotor

app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
def index():
	
	if request.method == 'POST':
		printBlue("Received POST with data:\n{}".format(request.get_json()))
		printGreen("Trying to turn motor...")

		motor = StepperMotor("high_speed")
		motor.turn(3)

		return render_template('index.html')
	elif request.method == 'GET':
		printGreen("Received GET...")
		return render_template('index.html')
	else:
		printError("Not GET nor POST!")

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)