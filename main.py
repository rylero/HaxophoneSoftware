import rtmidi
import time

out = rtmidi.MidiOut()
port = out.get_ports()[0]

def note_on_message(note, velocity, channel=0):
    return [0x90+channel, note, velocity]

def note_off_message(note, channel=0):
    return [0x80+channel, note, 0]

with out:
    for i in range(100):
        out.send_mesage(note_on_message(48, 127))
        time.sleep(1)
        out.send_mesage(note_off_message(48, 127))
        time.sleep(1)