# Description: This plays randomly shuffled music in a specificed directory.
# A pause and skip buttons are implemented assuming they are hooked up to
# GPIO pins 14 and 16, respectively.
# Date: December 6, 2020

# Imports
import RPi.GPIO as GPIO
from time import sleep
from numpy import random 
from pygame import mixer
from pathlib import Path

# mappen som innholder sangene
# /default-Home/din-raspberry-pi-brukenavn/mappen-navn/
MUSIC_DIR = '/home/passord123/Music/'

# samle inn sanger somer mp3 file type og random shuffle dem
mp3_path = Path(MUSIC_DIR)
mp3s = list(mp3_path.glob('*.mp3'))
assert len(mp3s) > 0, 'There were no mp3 files found in {}'.format(MUSIC_DIR)
random.shuffle(mp3s)

# Initialer knappene
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pause Button
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Hoppe over Button
           
# Initialer Mixeren
mixer.init()

# spill hvert sang i listene mens du trykk knappene
for song in mp3s:
        
    # laste og start å spille sanger
    mixer.music.load(str(song))
    mixer.music.play()
    
    # Mens sangen spiller...
    is_paused = False
    print('Now playing {}'.format(song))
    while mixer.music.get_busy():
        pause_state = GPIO.input(14)
        skip_state = GPIO.input(16)
        
        # Om Hoppe over knappen er trykket ...
        if not skip_state:
            print('Skipping to next song...')
            mixer.music.stop()
            sleep(0.20)
        
        # Om pause Knappen er trykket...
        if not pause_state:
            
            # Ta Pause eller Unpause tilsvarende
            if is_paused:
                print('Unpausing...')
                mixer.music.unpause()
                is_paused = False
            else:
                print('Pausing...')
                mixer.music.pause()
                is_paused = True
            
            # forsinkelse når pause knappen er trykket
            sleep(4)
            
print('Bye! Thanks for listening!')
exit()