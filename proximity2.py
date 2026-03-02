import RPi.GPIO as GPIO
import time

#GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.IN)
GPIO.setup(18, GPIO.OUT)

GPIO.output(14, GPIO.LOW)
time.sleep(0.1)

def measure_distance(timeout=0.023):
   #added a timeout variable
   #speed of sound 343m/s or 34300 cm/s
   #34300 cm/s x 0.023s = 789cm
   #789cm/2 = 394cm measurable (3.94m)(sensor max range 4m)
   #Trigger ultrasonic pulse
   GPIO.output(14, GPIO.HIGH)
   time.sleep(0.00001) #10 us pulse
   GPIO.output(14, GPIO.LOW)
   
   #change time.time() to time.perf_counter()
   t0 = time.perf_counter()

   #Measure the time for echo

   #Invalid measurement (too far, poor sound reflection)
   while GPIO.input(15) == 0:
      if time.perf_counter() - t0 > timeout:
         return None 
   
   start_time = time.perf_counter()

   #Echo pulse duration too long(stuck high)
   while GPIO.input(15) == 1:
      if time.perf_counter() - start_time > timeout:
         return None 
      
   end_time = time.perf_counter()
      
   #Calculate distance (in cm)
   elapsed_time = end_time - start_time
   distance = (elapsed_time * 34300) /2
   return distance
   
try:
   while True:
      dist = measure_distance()
      print("Distance:", dist, "cm")
      
      #Turn on LED if distance is less than 10 cm
      if dist is None:
         GPIO.output(18, GPIO.LOW)
      elif dist < 10:
         GPIO.output(18, GPIO.HIGH)
      else:
         GPIO.output(18, GPIO.LOW)
        
      time.sleep(1)  #delay before next reading
      
except KeyboardInterrupt:
   print("Exiting Program")
   GPIO.cleanup() #Reset GPIO settings
