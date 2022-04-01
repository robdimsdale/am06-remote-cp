import board
import pulseio
import adafruit_irremote

IR_PIN = board.IR_RX  # Pin connected to IR receiver.

LOW = 800
HIGH = 1600
FIRST = 2200

# see: https://learn.adafruit.com/ir-sensor/circuitpython
#      https://learn.adafruit.com/infrared-ir-receive-transmit-circuit-playground-express-circuit-python
pulses = pulseio.PulseIn(IR_PIN, maxlen=200, idle_state=True)

decoder = adafruit_irremote.GenericDecode()

pulses.clear()
pulses.resume()

first_part = [0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0]

commands = {
    "power":          [0,0,0,0,0,0,0,0,0,0,0,0],
    "oscillate":      [1,0,0,0,1,0,0,0,1,0,0,0],
    "fan_increase":   [0,0,1,0,0,0,1,0,0,0,1,0],
    "fan_decrease":   [1,0,1,0,1,0,1,0,1,0,1,0],
    "timer_increase": [0,0,1,0,1,0,1,0,1,0,0,0],
    "timer_decrease": [1,0,1,0,0,0,0,0,1,0,1,0]
}

last_part_1 = [0,0,0,0]
last_part_2 = [0,0,1,0]
last_part_3 = [1,0,0,0]

print('starting')

def process_pulses(pulses):
    if len(pulses) != 33:
        return

    else:
        mapped = []
        midpoint = (LOW+HIGH)/2
        for i, pulse in enumerate(pulses):
            if i == 0:
                mapped.append(2)
                continue

            if pulse > midpoint:
                mapped.append(1)
            else:
                mapped.append(0)

        first_part_subsection = mapped[1:17]
        command_subsection = mapped[17:29]
        last_part_subsection = mapped[29:33]

        if first_part_subsection != first_part:
            print('first part does not match: ', first_part_subsection)

        if last_part_subsection != last_part_1 and last_part_subsection != last_part_2 and last_part_subsection != last_part_3:
            print('last part does not match: ',last_part_subsection)

        found_command = ""
        for name, command in commands.items():
            if command == command_subsection:
                found_command = name
                print('matched: ', name)
                break

        if found_command == "":
            print('did not match any command: ', command_subsection)

# Loop waiting to receive pulses.
while True:
    # Wait for a pulse to be detected.
    detected = decoder.read_pulses(pulses)
    process_pulses(detected)

