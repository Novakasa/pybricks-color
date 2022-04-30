from pybricks.pupdevices import ColorDistanceSensor, Motor
from pybricks.parameters import Port, Color, Button
from pybricks.iodevices import PUPDevice
from pybricks.hubs import CityHub
from pybricks.tools import wait
import usys

lego_green = Color(132, 87, 55)
colors = [Color.GREEN, Color.WHITE, Color.BLACK, Color.BLUE, Color.YELLOW, Color.RED]
sensor_raw = PUPDevice(Port.B)
sensor_hsv = ColorDistanceSensor(Port.B)
motor = Motor(Port.A)
hub = CityHub()

data_size = 1500
data_rgb = (bytearray(data_size), bytearray(data_size), bytearray(data_size))

data_index = 0

def store_color():
    global data_index, data_rgb
    rgb_raw = sensor_raw.read(6)

    for rgb_index in range(3):
        entry = (rgb_raw[rgb_index]).to_bytes(2, "big")
        data_rgb[rgb_index][data_index] = entry[0]
        data_rgb[rgb_index][data_index+1] = entry[1]
    data_index += 2

hub.system.set_stop_button(None)

state = None

def set_state(p_state):
    global state
    print(p_state)
    if p_state == "measuring":
        hub.light.on(Color.YELLOW)
    if p_state == "waiting":
        hub.light.on(Color.GREEN)
    if p_state == "sending":
        hub.light.on(Color.BLUE)
    state = p_state

def start_measuring():
    set_state("measuring")
    motor.reset_angle(0)
    motor.run(900)

def finish_measuring():
    global data_index
    data_index = 0

    motor.stop()
    angle = motor.angle()
    print("motor angle:", angle)

    set_state("sending")
    print("data::")
    usys.stdout.buffer.write(data_rgb[0])
    usys.stdout.buffer.write(data_rgb[1])
    usys.stdout.buffer.write(data_rgb[2])
    print()
    set_state("waiting")
    motor.run(-900)
    wait(5400)
    motor.stop()

set_state("waiting")

while True:
    if hub.button.pressed():
        if state == "waiting":
            print("pressed")
            hub.light.on(Color.ORANGE)
            wait(1000)
            start_measuring()
        else:
            motor.stop()
            break
        wait(200)
    if state == "measuring":
        store_color()
        wait(5)
        if data_index==data_size:
            finish_measuring()
            # break
wait(1000)