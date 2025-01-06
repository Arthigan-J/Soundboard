import pygame
from gpiozero import Button

pygame.init()


button_sounds = {
    Button(26, bounce_time=0.05): pygame.mixer.Sound("samples/piano-c_C_major.wav"), 
    Button(6, bounce_time=0.05): pygame.mixer.Sound("samples/piano-b_B_major.wav"), 
    Button(4, bounce_time=0.05): pygame.mixer.Sound("samples/piano-a_A_major.wav")
}

for button, sound in button_sounds.items():
    button.when_pressed = sound.play

# Infinite loop to keep the program running and waiting for button presses
try:
    while True:
        pass  # Keep the program running indefinitely
except KeyboardInterrupt:
    pygame.quit()  # Gracefully exit on a KeyboardInterrupt (Ctrl+C)
