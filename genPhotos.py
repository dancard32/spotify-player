from PIL import Image, ImageDraw, ImageFont
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.request
from API_Key import API_KEY
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""" Globally loaded constants """
DEVICE_ID, CLIENT_ID, CLIENT_SECRET = API_KEY()

fid = open('CardData.json')
TrackData = json.load(fid)
fid.close()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri="http://localhost:8080",
                scope="user-read-playback-state,user-modify-playback-state"))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def genCardPhotos():
    blank_background = Image.open("assets/Blank_Card.png")

    for names in TrackData.values():
        background = blank_background.copy()
        tmp = names["name"]
        
        if names["type"].lower() == "playlist":
            results = sp.playlist_cover_image(names["url"])
            url = results[0]["url"]

        elif names["type"].lower() == "album":
            results = sp.album(names["url"])
            url = results["images"][0]["url"]

        elif names["type"].lower() == "track":
            results = sp.track(names["url"])
            url = results["album"]["images"][0]["url"]

        #urllib.request.urlretrieve(url, f"images/cards/cover_art/card_{tmp}.png")
        img = Image.open(f"images/cards/cover_art/card_{tmp}.png").resize((1500,1500))

        background.paste(img, (65, 375))

        draw = ImageDraw.Draw(background)
        myFont = ImageFont.truetype("Arial Bold.ttf", 128)
        w, h = draw.textsize(tmp, font=myFont)
        draw.text(((1629-w)/2, 0.05*2896), tmp, fill="black", font=myFont)

        background.save(f"images/cards/{tmp}.png")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def genPaperPrints():
    blank_background = Image.open("assets/Paper_Template.png")
    background = blank_background.copy()

    i = 0; j = 0; k = 0
    for names in TrackData.values():
        tmp = names["name"]
        img = Image.open(f"images/cards/{tmp}.png").rotate(90).resize((1125,630))
        
        if i == 2:
            i = 0
            j += 1
        if j != 6:
            background.paste(img, (i*500,j*100))
        
        
        background.save(f"images/pages/page_{k}.png")
        #background = blank_background.copy()

        #k += 1
        i += 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    #genCardPhotos()
    genPaperPrints()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    main()