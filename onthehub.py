from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Light
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = CityHub()

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll

motor = DCMotor(Port.A)
headlight = Light(Port.B)

# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

while True:

    # Optional: Check available input.
    while not keyboard.poll(0):
        # Optional: Do something here.
        wait(10)

    # Read one byte.
    cmd = stdin.buffer.read(1)

    # Decide what to do based on the command.
    if cmd == b"f":
        motor.dc(30)
    elif cmd == b"n":
        headlight.on(100)
    elif cmd == b"d":
        headlight.off()
    elif cmd == b"r":
        motor.dc(-40)
    elif cmd == b"s":
        motor.stop()
    elif cmd == b"b":
        break
    else:
        motor.stop()
    
    # Send a response.
    stdout.buffer.write(b"OK")