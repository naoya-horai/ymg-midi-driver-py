import time
import board
import digitalio
import busio
import usb_midi
import time


import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.control_change import ControlChange

class Button:
    """
    Midi Key Button
    """

    def __init__(self, pin, direction):
        self.status = False
        self.io_ = digitalio.DigitalInOut(pin)
        self.io_.direction = direction
    def pullup(self):
        self.io_.pull = digitalio.Pull.UP
    def value(self):
        return self.io_.value
    def hiz(self):
        self.io_.value = True
    def lowz(self):
        self.io_.value = False

Buttons = []

Buttons.append(Button(board.GP7, digitalio.Direction.OUTPUT))   # middle C
Buttons.append(Button(board.GP6, digitalio.Direction.OUTPUT))
Buttons.append(Button(board.GP5, digitalio.Direction.OUTPUT))
Buttons.append(Button(board.GP4, digitalio.Direction.OUTPUT))
Buttons.append(Button(board.GP0, digitalio.Direction.INPUT))   # middle C
Buttons.append(Button(board.GP1, digitalio.Direction.INPUT))
Buttons.append(Button(board.GP2, digitalio.Direction.INPUT))
Buttons.append(Button(board.GP3, digitalio.Direction.INPUT))
# Set USB MIDI up on channel 0
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
midinotes = [70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86]
# key press LED
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
buttonvalue =[True,True,True,True,
              True,True,True,True,
              True,True,True,True,
              True,True,True,True]
last_position = None
Buttons[0].lowz()
Buttons[1].lowz()
Buttons[2].lowz()
Buttons[3].lowz()



Buttons[4].pullup()
Buttons[5].pullup()
Buttons[6].pullup()
Buttons[7].pullup()


import time
while True:
    for i in range(2):
        Buttons[i].hiz()
        for j in range(4):
            if buttonvalue[j+ 4*i] != Buttons[j+4].value():
                # print(Buttons[j+4].value())
                #print("pressed")
                #print(Buttons[j+4].value())
                if Buttons[j+4].value():
                    #print("released")
                    #print(j+4*i)
                    midi.send(ControlChange(midinotes[j+ 4*i], 127))
                else:
                    #print("pushed")
                    #print(j+4*i)
                    midi.send(ControlChange(midinotes[j+ 4*i], 0))
            buttonvalue[j+ 4*i] = Buttons[j+4].value()
            print(buttonvalue)
            time.sleep(0.01)
        time.sleep(0.01)
        Buttons[i].lowz()