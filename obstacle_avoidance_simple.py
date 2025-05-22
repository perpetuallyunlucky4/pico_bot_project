from machine import Pin, PWM, time_pulse_us
import time

# Motor A (Left)
in1 = Pin(3, Pin.OUT)
in2 = Pin(2, Pin.OUT)
ena = PWM(Pin(4))

# Motor B (Right)
in3 = Pin(5, Pin.OUT)
in4 = Pin(6, Pin.OUT)
enb = PWM(Pin(7))

trig = Pin(8, Pin.OUT)
echo = Pin(9, Pin.IN)

ena.freq(1000)
enb.freq(1000)

def motorA_forward():
    in1.low()
    in2.high()

def motorA_backward():
    in1.high()
    in2.low()

def motorA_stop():
    ena.duty_u16(0)

def motorB_forward():
    in3.low()
    in4.high()

def motorB_backward():
    in3.high()
    in4.low()

def motorB_stop():
    enb.duty_u16(0)

def motorA_setspeed(speed):
    ena.duty_u16(int((speed/100)*65535))

def motorB_setspeed(speed):
    enb.duty_u16(int((speed/100)*65535))
    
def get_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    duration = time_pulse_us(echo, 1, 30000)
    distance = (duration * 0.0343) / 2
    return distance


try:
    while True:
        dist = get_distance()
        print("distance: ", dist, " cm")
        
        if dist < 10:
            print("object detected, avoiding")
            
            motorA_backward()
            motorB_backward()
            
            motorA_setspeed(50)
            motorB_setspeed(50)
            time.sleep(1)
            
            motorA_forward()
            motorB_backward()
            
            time.sleep(0.5)
            
        else:
            motorA_forward()
            motorB_forward()
            motorA_setspeed(70)
            motorB_setspeed(70)
            
        time.sleep(0.1)
except KeyboardInterrupt:
    print("cleaning up...")
    motorA_stop()
    motorB_stop()
