import rtmidi
import time
import json
from constants import IO_MAPPING
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def setup_io():
    for pin in IO_MAPPING.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def load_haxo_config():
    with open("haxoconfig.json", "r") as f:
        config = json.load(f)
    return config

def load_keymap(config: dict):
    key_mapping = {}
    for key in config["key_map"].keys():
        key_mapping[int(key)] = config["key_map"][key]
    return key_mapping

def note_on_message(note, velocity, channel=0):
    return [0x90+channel, note, velocity]

def note_off_message(note, channel=0):
    return [0x80+channel, note, 0]

def get_active_buttons():
    pressed = []
    for pin in IO_MAPPING.keys():
        if GPIO.input(pin):
            pressed.append(IO_MAPPING[pin])
    return pressed

def main():
    config = load_haxo_config()
    keymap = load_keymap(config)

    midiout = rtmidi.MidiOut()
    avaliable_ports = midiout.get_ports()

    if avaliable_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    currently_held = None

    while True:
        buttons_pressed = get_active_buttons()
        buttons_pressed.sort()

        for note in keymap.keys():
            buttons = keymap[note]
            if all(x == y for x, y in zip(buttons_pressed, buttons)):
                midiout.send_message(note_off_message(currently_held)) # turn off previous
                midiout.send_message(note_on_message(note, 127)) # turn on new note
                currently_held = note
                break

if __name__ == "__main__":
    main()