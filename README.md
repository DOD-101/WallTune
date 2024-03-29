# WallTune

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

<sub>Version: 0.1.0.0</sub>

## Features

- Gets your most recent spotify liked songs' Images
- Get the average color of an image to use as a fill color
- Auto-Sort the images based on color

- Simple to use && highly modular

## Usage

1. Create a spotify APP

2. Create a .env in spotify_api as such:

```  shell
SPOTIPY_CLIENT_ID=<your_client_id>
SPOTIPY_CLIENT_SECRET=<your_client_secret>
SPOTIPY_REDIRECT_URI=<your_redirect>
```

3. Run ```./spotify_api/main.py```

## To-Do
- add the ability for the scripts to create directories (isdir() -> false if dir !exists)

- write bash scripts

## Dependencies

See ```requirements.txt```

## Contributors

- Main Dev: David Thievon

Thanks to everyone who developed any of the dependencies and special thanks to the devs at Spotify for their great API.