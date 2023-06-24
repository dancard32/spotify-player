def readtext(fid):
    with open(f"{fid}.txt") as f:
        API = f.read()
    return API

def API_KEY():
    """
    Spotify's API Web Keys will be used across several python files
    In order to reduce error and increase ease of use, modify just this file
    and the rest of the python files will load these API Keys.
    """
    DEVICE_ID = readtext("DEVICE_ID")
    CLIENT_ID = readtext("CLIENT_ID")
    CLIENT_SECRET = readtext("CLIENT_SECRET")
    print(DEVICE_ID, type(DEVICE_ID))

    return DEVICE_ID, CLIENT_ID, CLIENT_SECRET