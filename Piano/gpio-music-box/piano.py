from signal import signal, SIGTERM, SIGHUP, pause
from smbus import SMBus
from time import sleep
import pygame
from gpiozero import Button

pygame.init()

def safe_exit(signum, frame):
    exit(1)

bus = SMBus(1)

ads7830_commands = [0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4]

def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    sleep(0.05)
    data = bus.read_i2c_block_data(0x4b, 0, 2)
    value = (data[0] << 8) | data[1]  
    return value

button_sounds = {
    Button(26, bounce_time=0.05): pygame.mixer.Sound("/home/arth/gpio-music-box/samples/piano-c_C_major.wav"), 
    Button(6, bounce_time=0.05): pygame.mixer.Sound("/home/arth/gpio-music-box/samples/piano-b_B_major.wav"), 
    Button(4, bounce_time=0.05): pygame.mixer.Sound("/home/arth/gpio-music-box/samples/piano-a_A_major.wav")
}

def get_volume_from_resistor(input):
    value = read_ads7830(input)
    volume = value / 255.0  
    print(f"Setting volume to {volume:.2f}")  
    return volume

def set_button_sound_volume():
    while True:
        for button, sound in button_sounds.items():
            volume = get_volume_from_resistor(0)  
            sound.set_volume(volume)
        sleep(0.2) 

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

for button, sound in button_sounds.items():
    button.when_pressed = sound.play

import threading
volume_thread = threading.Thread(target=set_button_sound_volume)
volume_thread.daemon = True  
volume_thread.start()

try:
    while True:
        pass  
except KeyboardInterrupt:
    pygame.quit()  # Exit on (Ctrl+C)