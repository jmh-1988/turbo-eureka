
# sudo pigpiod must be running

import pigpio
import time
import sys

PWM1 = 12   # Channel A
PWM2 = 19   # Channel B

FREQ = 100000                 # 100 kHz
PERIOD_US = int(1e6 / FREQ)  # 10 us

#DEAD_US = 1                  # 1 us dead time 
DEAD_US = 0.5                 # 500 ns dead time   
ON_US = (PERIOD_US // 2) - DEAD_US   # 4 us

pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    sys.exit(1)

pi.set_mode(PWM1, pigpio.OUTPUT)
pi.set_mode(PWM2, pigpio.OUTPUT)

wf = []

# Phase 1: PWM1 ON, PWM2 OFF
wf.append(pigpio.pulse(1 << PWM1, 1 << PWM2, ON_US))

# Dead time 1: both OFF
wf.append(pigpio.pulse(0, (1 << PWM1) | (1 << PWM2), DEAD_US))

# Phase 2: PWM1 OFF, PWM2 ON
wf.append(pigpio.pulse(1 << PWM2, 1 << PWM1, ON_US))

# Dead time 2: both OFF
wf.append(pigpio.pulse(0, (1 << PWM1) | (1 << PWM2), DEAD_US))

pi.wave_clear()
pi.wave_add_generic(wf)

wave_id = pi.wave_create()
if wave_id < 0:
    print("Failed to create wave")
    sys.exit(1)

pi.wave_send_repeat(wave_id)

print("Running complementary 100 kHz PWM on GPIO12 and GPIO19")
print("Dead time:", DEAD_US, "us")
print("Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Cleanup
pi.wave_tx_stop()
pi.wave_clear()
pi.write(PWM1, 0)
pi.write(PWM2, 0)
pi.stop()

print("Stopped.")
