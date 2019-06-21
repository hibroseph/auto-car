from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

print("Preparing servo, please wait")
kit.servo[1].angle = 90
kit.continuous_servo[0].throttle = 0
time.sleep(2)
	
print("Servo prepared, you can now enter a number from 0 to 1 indicating the speed at which you would like the servo to move")
print("I recommend starting at .2")
print("type q to quit the program")

x = 0
switched = 0



while(1):
    x = input()
    
    if x == 'q':
        print("Goodbye")
        break;
    kit.continuous_servo[0].throttle = float(x)
    time.sleep(0.1)


	
	
