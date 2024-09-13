import cv2
import socket
import math
import pickle
import serial
import sys
import time
#TODO: Import MPU and DistanceSensor libraries


class RPi_Client:
    def __init__(self):
        self.max_length = 65000
        self.host = ""
        self.port = 2222
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cap = cv2.VideoCapture(0)

        self.MICROBIT_PORT = 'COM5'
        self.BAUDRATE = 115200

        self.s = serial.Serial(self.MICROBIT_PORT)
        self.s.baudrate = self.BAUDRATE
        self.s.parity   = serial.PARITY_NONE
        self.s.databits = serial.EIGHTBITS
        self.s.stopbits = serial.STOPBITS_ONE

        self.velocity = [0, 0]
        self.heading = 0.0

        self.MPU = None
        self.DistanceSensor = None

        #TODO: Add MPU and DistanceSensor variables

    def updateVelocity(self, last_accel):
        for i in range(2):
            self.velocity[i] += last_accel[i] * 0.05
    
    def updateHeading(self):
        self.s.write(f'{self.heading}'.encode('utf-8'))
        data = self.s.readline().decode('UTF-8')
        data_list = data.rstrip().split(' ') # Heading only
        try:
            self.heading = float(data_list[0]) # might not need it because it's only one entry
        except:
            pass
    
    def sendPOV(self):
        data, address = self.sock.recvfrom(self.max_length)
        print(data.decode())

        ret, frame = self.cap.read()

        if ret:
            # compress frame
            retval, buffer = cv2.imencode(".jpg", frame)

            if retval:
                # convert to byte array
                buffer = buffer.tobytes()
                # get size of the frame
                buffer_size = len(buffer)
                num_of_packs = 1
                if buffer_size > self.max_length:
                    num_of_packs = math.ceil(buffer_size/self.max_length)

                frame_info = {
                            "packs" : num_of_packs,
                            "velocity" : self.velocity,
                            "heading" : self.heading
                            }
                
                # send the number of packs to be expected
                # print("Number of packs:", num_of_packs)
                self.sock.sendto(pickle.dumps(frame_info), (self.host, self.port))
                
                left = 0
                right = self.max_length

                for i in range(num_of_packs):
                    # print("left:", left)
                    # print("right:", right)

                    # truncate data to send
                    data = buffer[left:right]
                    left = right
                    right += self.max_length

                    # send the frames accordingly
                    self.sock.sendto(data, (self.host, self.port))
            
            ret, frame = self.cap.read()

    def run(self):
        while True:
            self.updateVelocity(self.MPU.accelerometer)
            self.updateHeading()
            self.sendPOV()
            time.sleep(0.05)

client = RPi_Client()

if __name__ == "__main__":
    client.run()