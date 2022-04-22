from time import sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""" Globally loaded constants """
DEVICE_ID="98bb0735e28656bac098d927d410c3138a4b5bca"
CLIENT_ID="96f4682ca85249e1874469dc3f310350"
CLIENT_SECRET="ca32c3e6ada2423485a28945d92d6f5b"
PLAY_PAUSE = True # True while playing, False while paused

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
def printInfo(data):
    print(f"Playing {data['item']['name']} by {data['item']['artists'][0]['name']}")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pausePlayTrack(channel):
    global PLAY_PAUSE
    
    print("Play/Pause")
    if PLAY_PAUSE:
        sp.pause_playback(device_id=DEVICE_ID)
        PLAY_PAUSE = False
    else:
        sp.start_playback(device_id=DEVICE_ID)
        PLAY_PAUSE = True
        info = sp.currently_playing()
        printInfo(info)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def skipTrack(channel):
    print("Skip track")
    sp.next_track(device_id=DEVICE_ID)
    info = sp.currently_playing()
    printInfo(info)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def backTrack(channel):
    print("Prior track")
    sp.previous_track(device_id=DEVICE_ID)
    info = sp.currently_playing()
    printInfo(info)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(11, GPIO.RISING, callback=pausePlayTrack)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(13 , GPIO.RISING, callback=skipTrack)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(15, GPIO.RISING, callback=backTrack)
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
            print("\nWaiting for record scan...")
            id = reader.read()[0]
            print(f"Card Value is: {id}")
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
            
            if id:
                url, name, type = parseRFID(id)
            if type == "Track":
                print(f"Playing {type}: {name}")
                sp.start_playback(device_id=DEVICE_ID, uris=[url])
                sleep(1)
                info = sp.currently_playing()
                printInfo(info)
            elif type == "Playlist" or type == "Album":
                print(f"Playing {type}: {name}")
                sp.start_playback(device_id=DEVICE_ID, context_uri=url)
                sp.shuffle(True, device_id=DEVICE_ID)
                sp.next_track()
                sleep(1)
                info = sp.currently_playing()
                printInfo(info)
                
    except Exception as e:
        print(e)
        pass
    
    finally:
        print("Cleaning up GPIO...")
        GPIO.cleanup()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~