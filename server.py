from flask import Flask, render_template, request, jsonify
from colored_printing import *
from stepper_motor import StepperMotor
import datetime
import time
import threading

alarmTime = "12:00"
alarmState = "off"

def waitForAlarmTime():
	global alarmTime
	currentTime = datetime.datetime.now().strftime("%H:%M")
	motor = StepperMotor("high_speed")	

	loopCount = 0

	while True:
		currentTime = datetime.datetime.now().strftime("%H:%M")
		if alarmState == "on" and alarmTime == currentTime:
			motor.turn("clockwise", 3)
			printGreen("Turning Motor!")
			if not loopCount % 5:
				printYellow("time = {}, state = {}".format(alarmTime, alarmState))
		time.sleep(2)

		if loopCount % 5 == 0:
			printYellow("time = {}, state = {}".format(alarmTime, alarmState))
		loopCount += 1

threading.Thread(target=waitForAlarmTime).start()

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def index():
	global alarmTime
	global alarmState
	if request.method == 'POST':
		printBlue("Received POST with data:\n{}".format(request.get_json()))

		alarmTime = datetime.datetime.strptime(request.get_json()["time"], "%H:%M").strftime("%H:%M")
		alarmState = request.get_json()["alarmState"]
		print("request.get_json()['alarmState'] = ", request.get_json()["alarmState"])

		return render_template('index.html')
	elif request.method == 'GET':
		printGreen("Received GET...")
		return render_template('index.html')
	else:
		printError("Not GET nor POST!")

@app.route('/test',methods = ['GET','POST'])
def test():
	return render_template('test.html')

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)