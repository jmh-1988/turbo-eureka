import RPi.GPIO as GPIO
import time

#GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.IN)
GPIO.setup(18, GPIO.OUT)

def measure_distance():
   #Trigger ultrasonic pulse
   GPIO.output(14, GPIO.HIGH)
   time.sleep(0.00001) #10 us pulse
   GPIO.output(14, GPIO.LOW)
   
   #Measure the time for echo
   while GPIO.input(15) == 0:
      start_time = time.time()
   while GPIO.input(15) == 1:
      end_time = time.time()
      
   #Calculate distance (in cm)
   elapsed_time = end_time - start_time
   distance = (elapsed_time * 34300) /2
   return distance
   
try:
   while True:
      dist = measure_distance()
      print("Distance:", distance, "cm")
      
      #Turn on LED if distance is less than 10 cm
      if dist < 10:
         GPIO.output(18, GPIO.HIGH)
      else:
         GPIO.output(18, GPIO.LOW)
        
      time.sleep(1)  #delay before next reading
      
except KeyboardInterrupt:
   print("Exiting Program")
   GPIO.cleanup() #Reset GPIO settings
      
   
      