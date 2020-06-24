from adafruit_circuitplayground import cp
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet

# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.color_packet import ColorPacket


import adafruit_fancyled.adafruit_fancyled as fancy
import adafruit_fancyled.fastled_helpers as helper
from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile
import board
import time

# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket

import time

ble = BLERadio()
uart_service = UARTService()
ble.name = "BabyYoda"
# uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)
advertisement.complete_name = "BabyYoda"

RainbowStripeColors = [
    0xFF0000, 0x000000, 0xAB5500, 0x000000,
    0xABAB00, 0x000000, 0x00FF00, 0x000000,
    0x00AB55, 0x000000, 0x0000FF, 0x000000,
    0x5500AB, 0x000000, 0xAB0055, 0x000000]

color = (0, 0, 255)

RED = (255, 0, 0)
ORANGE = (255, 50, 0)
YELLOW = (255, 165, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
INDIGO = (50, 0, 255)
VIOLET = (75, 0, 130)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

colors = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]

offset = 0  # Position offset into palette to make it "spin"

def playfile(filename):
    wave_file = open("/sounds/"+filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                brightPulse()
            cp.pixels.fill(BLACK)

def brightPulse():
    print("I'm about to brightPulse")
    global offset
    for i in range(10):
        color = fancy.palette_lookup(RainbowStripeColors, offset + i / 9)
        cp.pixels[i] = color.pack()
    time.sleep(0.15)
    cp.pixels.show()
    offset += 0.033  # Bigger number = faster spin
    print(offset)

while True:
    print("WAITING...")
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    while ble.connected:
        print("CONNECTED!")
        
        # Check for incoming message
        connection = ble.connections[0]
        uart = connection[UARTService]
        incoming_bytes = uart.in_waiting
        if incoming_bytes:
            bytes_in = uart.read(incoming_bytes)
            print("Received: ", bytes_in)
            in_label.text = in_label.text[incoming_bytes:] + bytes_in.decode()
        
        # Keeping trying until a good packet is received
        try:
            packet = Packet.from_stream(uart_server)
            print("Got a packet!", packet)
        except ValueError:
            continue

        if isinstance(packet, ColorPacket):
                print(packet.color)
                cp.pixels.fill((packet.color))
                color = packet.color
                print("color = ", color)

        # Only handle button packets
        if isinstance(packet, ButtonPacket) and packet.pressed:
            if packet.button == ButtonPacket.UP:
                print("Button UP")
                print("A1 touched!")
                #cp.play_file("/sounds/sparkle.wav")
                playfile("sparkle.wav")
            if packet.button == ButtonPacket.DOWN:
                print("Button DOWN")
                cp.pixels.fill((color))
                print("A2 Touched!")
                cp.play_file("/sounds/I_am_groot_1.wav")
                cp.pixels.fill((0, 0, 0))
            if packet.button == ButtonPacket.LEFT:
                print("Button LEFT")
            if packet.button == ButtonPacket.RIGHT:
                print("Button RIGHT")
            if packet.button == ButtonPacket.BUTTON_1:
                print("Button 1")
                cp.pixels.fill((color))
                print("A2 Touched!")
                cp.play_file("/sounds/scream.wav")
                cp.pixels.fill((0, 0, 0))
            if packet.button == ButtonPacket.BUTTON_2:
                print("Button 2")
            if packet.button == ButtonPacket.BUTTON_3:
                print("Button 3")
            if packet.button == ButtonPacket.BUTTON_4:
                print("Button 4")

    # Disconnected
    print("DISCONNECTED")
