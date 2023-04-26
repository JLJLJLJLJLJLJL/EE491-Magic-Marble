import pygame
import RPi.GPIO as GPIO

# Set up GPIO pins for the servos
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.output(8, GPIO.LOW)

# Initialize the pygame library
pygame.init()

# Set up the joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Set up the servos
servo1 = GPIO.PWM(16, 50)
servo2 = GPIO.PWM(18, 50)

servo1Start = 7.5
servo2Start = 7.5

servo1.start(servo1Start)
servo2.start(servo2Start)

trigger = False

try:
    while True:
        
        # Get joystick events
        for event in pygame.event.get():
            print(event)
            #Check if trigger is pressed for reset motor
            if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                trigger = not trigger
            
            #Check if trigger has been released
            #if event.type == pygame.JOYBUTTONUP and event.button == 0:
             #   trigger = False
            
            #If trigger is pressed, run reset motor and level maze
            if trigger:
                GPIO.output(8, GPIO.HIGH)
                servo1.ChangeDutyCycle(servo1Start)
                servo2.ChangeDutyCycle(servo2Start)
                break
                
            #If trigger is not pressed, stop motor
            if not trigger:
                GPIO.output(8, GPIO.LOW)
                
            # Check if joystick axis was moved
            if event.type == pygame.JOYAXISMOTION:
                # Move servo 1 based on Y-axis of left joystick
                if event.axis == 0:
                    servo1.ChangeDutyCycle(servo1Start + -(round(event.value, 2) * 4.5))
                    
                # Move servo 2 based on Y-axis of right joystick
                elif event.axis == 1:
                    servo2.ChangeDutyCycle(servo2Start + (round(event.value, 2) * 4.5))

except KeyboardInterrupt:
    # Clean up GPIO pins and quit pygame
    GPIO.cleanup()
    joystick.quit()
    pygame.quit()
