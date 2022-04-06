#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from time import sleep
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""" Globally loaded constants """
DEVICE_ID="98bb0735e28656bac098d927d410c3138a4b5bca"
CLIENT_ID="96f4682ca85249e1874469dc3f310350"
CLIENT_SECRET="ca32c3e6ada2423485a28945d92d6f5b"

fid = open('CardData.json')
TrackData = json.load(fid)
fid.close()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseRFID(id):
    url = TrackData[str(id)]["url"]
    name = TrackData[str(id)]["name"]
    type = TrackData[str(id)]["type"]

    return url, name, type
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""" Main loop on start up """
while True:
    try:
        reader = SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri="http://localhost:8080",
                scope="user-read-playback-state,user-modify-playback-state"))
        

        """ Loop to read in RFID Card's """
        while True:
            print("Waiting for record scan...")
            id = reader.read()[0]
            print(f"Card Value is: {id}")
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
            
            
            if id:
                url, name, type = parseRFID(id)

            if type == "Track":
                print(f"Playing {type}: {name}")
                sp.start_playback(device_id=DEVICE_ID, uris=[url])
                sleep(1)

            elif type == "Playlist" or type == "Album":
                print(f"Playing {type}: {name}")
                sp.start_playback(device_id=DEVICE_ID, context_uri=url)
                sp.shuffle(True, device_id=DEVICE_ID)
                sp.next_track()
                sleep(1)

    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning up GPIO...")
        GPIO.cleanup()