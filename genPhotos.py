from PIL import Image, ImageDraw, ImageFont # PIL library to modify images
import urllib.request                   # Python library to save images
import spotipy                          # Spotipy's python module
from spotipy.oauth2 import SpotifyOAuth # Allows authentication of Spotify
import json                             # Used to input CardData.json
from API_Key import API_KEY             # Allows constants across scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""" Globally loaded constants """
DEVICE_ID, CLIENT_ID, CLIENT_SECRET = API_KEY()

fid = open('CardData.json') # Open the .json data
TrackData = json.load(fid)  # Load the .json
fid.close()                 # Close out

# Authenticate spotipy to pull images
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri="http://localhost:8080",
                scope="user-read-playback-state,user-modify-playback-state"))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def genCardPhotos(PullSpotify):
    """
    genCardPhotos generates the Card stacks that will be printed and placed on
    top of the RFID cards. This function can either use custom photos or scrape
    images from Spotify if desired.

    Attributes:
        PullSpotify (bool): True if want default Spotify images

    Notes:
        Custom images must be cropped to a square ratio and saved with the name
        "CardData.json UNIQUE NAME.png" and located in "images/cards/cover_art"
    """

    blank_background = Image.open("assets/Blank_Card.png") # Template card

    # Loop through all songs/playlists/albums in CardData.json
    for names in TrackData.values():
        background = blank_background.copy()
        tmp = names["name"]
         
        # If using Spotify default images
        if PullSpotify:
            # Determine the url for each type of music
            if names["type"].lower() == "playlist":
                results = sp.playlist_cover_image(names["url"])
                url = results[0]["url"]

            elif names["type"].lower() == "album":
                results = sp.album(names["url"])
                url = results["images"][0]["url"]

            elif names["type"].lower() == "track":
                results = sp.track(names["url"])
                url = results["album"]["images"][0]["url"]

            # Save the photo locally
            urllib.request.urlretrieve(url, f"images/cards/cover_art/{tmp}.png")
        img = Image.open(f"images/cards/cover_art/{tmp}.png").resize((1500,1500))

        background.paste(img, (165, 375))

        # Add Card's name to the image
        draw = ImageDraw.Draw(background)
        myFont = ImageFont.truetype("Arial Bold.ttf", 128)
        w, h = draw.textsize(tmp, font=myFont)
        draw.text(((1629-w)/2, 0.05*2896), tmp, fill="black", font=myFont)
        background = background.resize((913, 1448)) # Downsize to fit paper_template

        background.save(f"images/cards/card_{tmp}.png")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def genPaperPrints():
    """
    genPaperPrints uses the custom card stack images and overlays them onto a
    page with sized cutouts to paste onto the RFID cards.
    """

    # Load blank template
    blank_background = Image.open("assets/Paper_Template.png")
    background = blank_background.copy()

    # Initialize enumerators
    i = 0; j = 0; k = 0
    for names in TrackData.values():
        # Obtain the name of the playlist/album/track and open associated image
        tmp = names["name"]
        img = Image.open(f"images/cards/card_{tmp}.png").rotate(90, expand=True)
        
        # Reset counter
        if i == 2: i = 0; j += 1

        # Continually paste cards onto the template
        if j != 4:
            background.paste(img, (215 + i*(300+1448+30),147 + j*(250+913+26)))
            i += 1
        
        # If bottom of the page is met, save and load a new template
        elif j == 4:
            background.save(f"images/pages/page_{k}.png")
            background = blank_background.copy()

            # First image of the next page
            i = 0; j = 0; k += 1
            background.paste(img, (215 + i*(300+1448+30),147 + j*(250+913+26)))
            i += 1
    # Save image regardless of how many cards on last page
    background.save(f"images/pages/page_{k}.png")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    PullSpotifyData = False
    genCardPhotos(PullSpotifyData)
    genPaperPrints()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    main()