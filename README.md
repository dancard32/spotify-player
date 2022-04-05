# spotify-player

## Description
This project is intended to expand an option on the google maps "Directions" functionality to provide a more sight-seeing experience for integration on road trips for a more immersive UX. This project was written in Python, and I am currently working to expand it to a static *github.io pages* website with a Flask back-end React front-end. 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Installation
Two installations are needed to run this locally

In order to run *main.py* [Python Client for Google Maps Services](https://pypi.org/project/googlemaps/) needs to be locally installed
```
pip install -U googlemaps
```

To plot and export *.html* data [A matplotlib-like interface to plot data with Google Maps](https://pypi.org/project/gmplot/) needs to be installed
```
pip install gmplot
```


## Usage
### API Key
I've IP restricted this API key to my personal computer, so if you would like to run this on your own local machine, *git clone* this repository and create a Google Cloud Platform project. This will be the project needed to get the api key. The Google Maps APIs you will need are:
* Directions API
* Geocoding API
* Maps JavaScript API
* Maps Static API
* Places API

After obtaining the API key replace the placeholder API key in *main.py*
### Checking Tourist Routes
If this is being ran locally, the results will be exported to *(root)/map.html*. To allow automatic refreshing use [Live-Server](https://github.com/ritwickdey/vscode-live-server) to open the *map.html* on a localhost that automatically updates every time the *main.py* is ran.
![Live Server](assets/liveServer.png)

<br />

**Example:** From University of Southern California to Griffith Observatory, the localhost *map.html* will look something like this
![LocalHost HTML](assets/liveHTML.png)

---
## License
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) prohibits the use of this for commercialization, but allows downloading editing/sharing amongst the community. If there is a request to commercialize, contact me personally via email at [dcard@umich.edu](mailto:dcard@umich.edu)
