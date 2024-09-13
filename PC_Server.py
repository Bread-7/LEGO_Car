import cv2
import socket
import pickle
import numpy as np
import sys

class PC_Server:
    def __init__(self):
        self.host = "" # Add back after push
        self.port = 2222
        self.max_length = 65540
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        self.frame_info = None
        self.buffer = None
        self.frame = None

    def outputData(self):
        data, address = self.sock.recvfrom(self.max_length)

        self.sock.sendto('test string'.encode(), address)
        
        if len(data) < 100:
            frame_info = pickle.loads(data)

            if frame_info:
                nums_of_packs = frame_info["packs"]

                for i in range(nums_of_packs):
                    data, address = self.sock.recvfrom(self.max_length)

                    if i == 0:
                        buffer = data
                    else:
                        buffer += data

                frame = np.frombuffer(buffer, dtype=np.uint8)
                frame = frame.reshape(frame.shape[0], 1)

                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                frame = cv2.flip(frame, 1)
                
                if frame is not None and type(frame) == np.ndarray:
                    text = f'Vel_X: {frame_info["velocity"][0]}\n' + \
                            f'Vel_Y: {frame_info["velocity"][1]}\n' + \
                            f'Heading: {frame_info["heading"]}'
                    cv2.putText(frame, text, (0, 0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
                    cv2.imshow("Stream", frame)
                    if cv2.waitKey(1) == 27:
                        sys.exit()