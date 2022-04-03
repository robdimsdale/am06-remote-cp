import board
import pulseio
import time
import array

from adafruit_circuitplayground.express import cpx

LOW = 775
HIGH = 1550
FIRST = 2250

pulseout = pulseio.PulseOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)

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

def create_pulse(command):
    command_pulse = commands[command]

    global current_last_part_index
    last_past_pulse = last_part[current_last_part_index]

    logical_pulse = first_part.copy()
    logical_pulse.extend(command_pulse)
    logical_pulse.extend(last_past_pulse)

    current_last_part_index = current_last_part_index + 1
    current_last_part_index = current_last_part_index % 3

    mapped_pulse = [FIRST]
    for i in logical_pulse:
        if i == 0:
            val = LOW
        else:
            val = HIGH
        mapped_pulse.append(val)

    return mapped_pulse

button_already_pressed = False
print('initialization complete')
while True:
    command = ""
    if cpx.switch:
        if cpx.button_a:
            command = "oscillate"
        elif cpx.button_b:
            command = "power"
        else:
            command = ""
            button_already_pressed = False
    else:
        if cpx.button_a:
            command = "fan_increase"
        elif cpx.button_b:
            command = "fan_decrease"
        else:
            command = ""
            button_already_pressed = False

    if command != "" and not button_already_pressed:
        mapped_pulse = create_pulse(command)
        cpx.red_led = True

        pulseout.send(array.array('H', mapped_pulse))
        cpx.red_led = False

        button_already_pressed = True
