#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

###################################
# CONFIGURING MOTORS AND SENSORS  #
###################################

# Configure the gripper motor on Port A.
# Configure the track motor on Port D.
gripper_motor = Motor(Port.A)
trackMotor = Motor(Port.D)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation
# of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

#Same es elbow just different values for gears.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations. This results in
# very smooth motion.
elbow_motor.set_run_settings(50, 120)
base_motor.set_run_settings(50, 120)

# Set up the Touch Sensor. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the elbow
# is in the starting position. This is when the sensor sees the
# white beam up close.
elbow_sensor = ColorSensor(Port.S3)

###################################
# INITIALIZATION                  #
###################################

# Initialize the elbow. First make it go down for 500 ms.
# Then make it go upwards slowly (15 degrees per second) until
# the Color Sensor detects the white beam. Then reset the motor
# angle to make this the zero point. Finally, hold the motor
# in place so it does not move.
elbow_motor.run_time(-30, 500)
elbow_motor.run(15)
while elbow_sensor.reflection() < 32:
    wait(10)
elbow_motor.reset_angle(0)
elbow_motor.stop(Stop.HOLD)

# Initialize the base. First rotate it until the Touch Sensor
# in the base is pressed. Reset the motor angle to make this
# the zero point. Then hold the motor in place so it does not move.
base_motor.run(-60)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.stop(Stop.HOLD)

# Initialize the gripper and track. First rotate the motor until it stalls.
# Stalling means that it cannot move any further. This position
# corresponds to the closed position. Then rotate the motor
# by 90 degrees such that the gripper is open.
gripper_motor.run_until_stalled(200, Stop.COAST, 50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(200, -90)

# Run track (we want track to run continuously)
trackMotor.run(140) 

###########################################
#   DEFINING FUNCTIONS  AND DESTINATIONS  #
###########################################


def robot_pick(position):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, closes the gripper, and
    # raises the elbow to pick up the object.
    # Rotate to the pick-up position.
    base_motor.run_target(60, position, Stop.HOLD)
    # Lower the arm.
    elbow_motor.run_target(60, -40)
    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(200, Stop.HOLD, 50)
    # Raise the arm to lift the wheel stack.
    elbow_motor.run_target(80, 0, Stop.HOLD)

def robot_release(position):
    # This function makes the robot base rotate to the indicated
    # position. There  opens the gripper to
    # release the object. Then it raises its arm again.
    # Rotate to the drop-off position.
    base_motor.run_target(60, position, Stop.HOLD)
    #This one sparks joy!
    elbow_motor.run_target(60, -5, Stop.HOLD)
    # Open the gripper to release the wheel stack.
    gripper_motor.run_target(200, -90)

# Play three beeps to indicate that the initialization is complete.
brick.sound.beeps(3)

# Define destinations for picking up and moving the wheel stacks.
MIDDLE = 100
RIGHT = 4
LEFT = 200

# This is the main part of the program. It is a loop that repeats endlessly.
#
# First, the robot moves the object on the left towards to the track on right.
while True:
    robot_pick(LEFT)
    robot_release(RIGHT)