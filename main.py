import RPi.GPIO as GPIO

import requests
import time

from SR04 import SR04_Ultrasonic as Ultrasonic_Sensor

class Ultra_Measure(object):

    def __init__(self, device_num):
        self.distance_detector = Ultrasonic_Sensor.Ultrasonic_Avoidance()

        # SET GPIO WARNINGS AS FALSE
        GPIO.setwarnings(False)

        # SET DEVICE ID 
        self.device_id = device_num
 
        # SETUP REQUEST DATA
        self.url = 'http://192.168.1.24:52275/data'
        self.datas = {'device_id' : device_num, 'status' : -1}
        self.headers = {'Contect-Type': 'application/json'}

        # CREATE SESSION
        self.sess = requests.Session()

        # SET WAIT_BOOL AS FALSE
        self.wait_bool = False

    def get_ultra_distance(self):
        return self.distance_detector.get_distance()

    def update_time_table(self):
        self.datas = {'device_id' : self.device_id, 'status' : 0}
        print(self.datas)
         
    def send_data(self):
        try:
            request_id = self.sess.post(self.url, json=self.datas, headers=self.headers)
            print(request_id.status_code)
        except requests.exceptions.RequestException as e:
            print(e)

    def get_wait_bool(self):
        return self.wait_bool

    def recv_reset_info(self):
        request_get = requests.get('https://192.168.1.24:52275/reset.html')
        if (request_get.status_code == 200): # 200 is OK
            request_info = request_get.headers
            if (request_info in "WAIT"):
                self.wait_bool = True
            elif (request_info in "READY"):
                self.wait_bool = False
        else:
            print(request_get.status_code)
            print("CONNECTION ERROR")


if __name__ == "__main__":
    try:
        um = Ultra_Measure(1)
        while True:
            distance_value = um.get_ultra_distance()
            # print(distance_value) # Test Print

            if distance_value > 0 and distance_value < 25:
                try:
                    um.update_time_table() # Perform Json data setup tasks
                finally:
                    um.send_data() # Transferring data to the server
                    
                   # while True: # Finite waiting until completion
                   #     um.recv_reset_info()
                   #     time.sleep(0.01)
                   #     if (self.wait_bool == False):
                   #         break

            time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()
