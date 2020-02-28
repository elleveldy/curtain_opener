import time
import sys
from gpiozero import OutputDevice as stepper


class StepperMotor():
	"""docstring for StepperMotor"""
	def __init__(self, speedMode):
		self.STEPS_PR_LOOP = 512
		self.LOOP_SIZE = 8
		self.SHORT_LOOP_SIZE = 4
		
		self.mode = speedMode
		if self.mode == "high_torque":
			self.sequence = 	[[1,0,0,1], # Define step sequence as shown in manufacturers datasheet
							 [1,0,0,0], 
							 [1,1,0,0],
							 [0,1,0,0],
							 [0,1,1,0],
							 [0,0,1,0],
							 [0,0,1,1],
							 [0,0,0,1]]
			self.STEPS_PR_LOOP = 512
			self.LOOP_SIZE = 8

		elif self.mode == "high_speed":
			self.sequence = 	[[1,0,0,0], # Define step sequence as shown in manufacturers datasheet
								 [0,1,0,0],
								 [0,0,1,0],
								 [0,0,0,1]]	
			self.STEPS_PR_LOOP = 512
			self.LOOP_SIZE = 4

		self.stepPins = [ stepper(12),stepper(16),stepper(20),stepper(21)] # Motor GPIO pins</p><p>

	def execute_step(self, step):
		for pin in self.sequence[step]:

			xPin = self.stepPins[pin]
			if self.sequence[step][pin] == 1:
				xPin.on
			else:
				xPin.off

	def turn(self, direction, nr_turns):
		nr_steps = int(nr_turns * self.STEPS_PR_LOOP * self.LOOP_SIZE)
		for i in range(0, nr_steps-1):                      
			step = i % self.LOOP_SIZE
			# step_nr = i % self.LOOP_SIZE if direction == "clockwise" else (self.LOOP_SIZE - 1) - i % self.LOOP_SIZE 
			if direction == "clockwise":
				step_nr = i % self.LOOP_SIZE
			elif direction == "counter_clockwise":
				step_nr = (self.LOOP_SIZE - 1) - i % self.LOOP_SIZE
			for pin in range(0,4):

				if self.sequence[step][pin]:
					self.stepPins[pin].on()
				else:
					self.stepPins[pin].off()
			time.sleep(0.002)

