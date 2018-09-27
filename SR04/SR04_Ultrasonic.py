import RPi.GPIO as GPIO
import time

class Ultrasonic_Avoidance(object):
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        # GPIO PIN SETUP
        self.trigger_pin = 33
        self.echo_pin = 32

        # TIMEOUT VALUE SETUP
        self.timeout = 0.1

    def get_distance(self):
        pulse_end = 0
        pulse_start = 0

        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.01)
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
        GPIO.setup(self.echo_pin, GPIO.IN)

        timeout_start = time.time()
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1

        if pulse_start != 0 and pulse_end != 0:
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 100 * 343.0 / 2
            distance = int(distance)
            

            if distance >= 0:
                return distance
            else:
                return -1
        else:
            return -1


if __name__ == "__main__":
    try:
        distance_detector = Ultrasonic_Avoidance()
        while True:
            print(distance_detector.get_distance())
            time.sleep(0.01)

    except KeyboardInterrupt:
        GPIO.cleanup()
