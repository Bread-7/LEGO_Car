import numpy as np

# Default distance units: customary

class Constants:
    def __init__(self):
        self.MICROBIT_PORT = 'COM5'
        self.BAUDRATE = 115200
        self.ANGLE_MOTOR_PORT = 'A'
        self.DRIVE_MOTOR_PORT = 'B'
        self.CONTROLLER_ID = 0
        self.LEFT_Y_AXIS = 1
        self.RIGHT_X_AXIS = 2
        self.DRIVE_CIRCUMFERENCE = 1.4 * np.pi
        self.ANGLE_CIRCUMFERENCE = 2.55906 * np.pi
        self.MAX_WHEEL_ANGLE = 19
        self.DRIVE_GEAR_RATIO = 9 / 25

        # TODO: Workshop vals
        self.MAX_RPM = 0.0
        self.MIDPOINT_DEG = 0.0
        self.MAX_CCW_DEG = 0.0
        self.MAX_CW_DEG = 0.0
        self.DELTA_CCW = np.abs(self.MIDPOINT_DEG - self.MAX_CCW_DEG)
        self.DELTA_CW = np.abs(self.MIDPOINT_DEG - self.MAX_CW_DEG)
