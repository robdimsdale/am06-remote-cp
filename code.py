import board
import pulseio
import adafruit_irremote
import time
import array

from adafruit_circuitplayground.express import cpx

LOW = 775
HIGH = 1550
FIRST = 2250

# see: https://learn.adafruit.com/ir-sensor/circuitpython
#      https://learn.adafruit.com/infrared-ir-receive-transmit-circuit-playground-express-circuit-python
pulses = pulseio.PulseIn(board.IR_RX, maxlen=50, idle_state=True)
pulses.clear()
pulses.resume()

pulseout = pulseio.PulseOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)

decoder = adafruit_irremote.GenericDecode()

first_part = [0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0]

commands = {
    "power":          [0,0,0,0,0,0,0,0,0,0,0,0],
    "oscillate":      [1,0,0,0,1,0,0,0,1,0,0,0],
    "fan_increase":   [0,0,1,0,0,0,1,0,0,0,1,0],
    "fan_decrease":   [1,0,1,0,1,0,1,0,1,0,1,0],
    "timer_increase": [0,0,1,0,1,0,1,0,1,0,0,0],
    "timer_decrease": [1,0,1,0,0,0,0,0,1,0,1,0]
}

last_part = [
  [0,0,0,0],
  [0,0,1,0],
  [1,0,0,0]
]

current_last_part_index = 0

print('starting')

def create_pulse(command):
    command_pulse = commands[command]
    
    global current_last_part_index
    last_past_pulse = last_part[current_last_part_index]
    
    logical_pulse = first_part.copy()
    logical_pulse.extend(command_pulse)
    logical_pulse.extend(last_past_pulse)
    
    current_last_part_index = current_last_part_index + 1
    current_last_part_index = current_last_part_index % 3
    
    #print('logical pulse: ', logical_pulse)
    
    mapped_pulse = [FIRST]
    for i in logical_pulse:
        if i == 0:
            val = LOW
        else:
            val = HIGH
        mapped_pulse.append(val)
        
    #print('mapped pulse: ', mapped_pulse)
    
    return mapped_pulse

while True:
    ###
    mapped_pulse = create_pulse("oscillate")
    
    cpx.red_led = True
   
    print('sending pulse: ', mapped_pulse)
    pulseout.send(array.array('H', mapped_pulse))
    print('sending done')
    cpx.red_led = False
    
    time.sleep(4)

