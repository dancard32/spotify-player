from mfrc522 import SimpleMFRC522       # Python module to read RFID tags
import RPi.GPIO as GPIO                 # Allows RPi to interface with GPIO
from time import sleep                  # Timeout to wait for web API call
import spotipy                          # Spotipy's python module
from spotipy.oauth2 import SpotifyOAuth # Allows authentication of Spotify
import json                             # Used to input CardData.json
from API_Key import API_KEY             # Allows constants across scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""" Globally loaded constants """
DEVICE_ID, CLIENT_ID, CLIENT_SECRET = API_KEY()
PLAY_PAUSE = True # True while playing, False while paused

fid = open('CardData.json') # Open the .json data
TrackData = json.load(fid)  # Load the .json
fid.close()                 # Close out
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseRFID(id):
    """
    parseRFID inputs the RFID hash ID and returns the url, associated name, and
    the type of music (either playlist/track/album).

    Attributes:
        id (int): The integer value read in via the GPIO pins of the RPi
    """
    url = TrackData[str(id)]["url"]
    name = TrackData[str(id)]["name"]
    type = url.split(":")[1].lower()

    return url, name, type
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printInfo(data):
    """
    printInfo prints to terminal the music data

    Attributes:
        data (dict): The returned data via the Spotify Web API
    """
    print(f"Playing {data['item']['name']} by {data['item']['artists'][0]['name']}")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pausePlayTrack(channel):
    """
    pausePlayTrack GPIO callback function to allow RPi to play or pause music
    through spotify

    Attributes:
        channel (BOARD): Inhereted from GPIO.setmode(GPIO.BOARD)
    """
    global PLAY_PAUSE   # global variable to allow several function callbacks

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
    """
    skipTrack GPIO callback function to allow RPi to skip current track

    Attributes:
        channel (BOARD): Inhereted from GPIO.setmode(GPIO.BOARD)
    """

    print("Skip track")
    sp.next_track(device_id=DEVICE_ID)
    info = sp.currently_playing()
    printInfo(info)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def backTrack(channel):
    """
    backTrack GPIO callback function to allow RPi to go to previous track

    Attributes:
        channel (BOARD): Inhereted from GPIO.setmode(GPIO.BOARD)
    """

    print("Previous track")
    sp.previous_track(device_id=DEVICE_ID)
    info = sp.currently_playing()
    printInfo(info)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""" RPi set-up to allow button pushing """
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# GPIO setup on PIN 11 to play/pause music
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(11, GPIO.RISING, callback=pausePlayTrack)

# GPIO setup on PIN 13 to skip the current track
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(13 , GPIO.RISING, callback=skipTrack)

# GPIO setup on PIN 15 to play the previous track
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

        # Loop to read in RFID Card's
        while True:
            print("\nWaiting for record scan...")

            id = reader.read()[0]
            print(f"Card Value is: {id}")
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

            # Once the RFID card is read, parse the data for music selection
            if id: url, name, type = parseRFID(id)

            # If track type is selected play the track
            if type == "track":
                print(f"Playing {type}: {name}")
                sp.start_playback(device_id=DEVICE_ID, uris=[url])
                sleep(1)
                info = sp.currently_playing()
                printInfo(info)

            # With Playlist/Album type use context_uri and enable shuffle
            elif type == "playlist" or type == "album":
                print(f"Playing {type}: {name}")
                sp.start_playback(device_id=DEVICE_ID, context_uri=url)
                sp.shuffle(True, device_id=DEVICE_ID)
                sp.next_track()
                sleep(1)
                info = sp.currently_playing()
                printInfo(info)

    # Print the error and continue the loop
    except Exception as e:
        print(e)
        pass

    # Cleanup the GPIO input for the next RFID card to be read
    finally:
        print("Cleaning up GPIO...")
        GPIO.cleanup()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~