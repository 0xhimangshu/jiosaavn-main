<div align="center">
  <img src="assets/banner.png" alt="JioSaavn CLI" width="800"/>

  # Saavn.py

  A modern command-line interface for JioSaavn music downloads

  [![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg?style=flat-square&logo=python)](https://www.python.org)
  [![MIT License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)
  [![PyPI version](https://img.shields.io/pypi/v/saavn.py.svg?style=flat-square)](https://pypi.org/project/saavn.py/)
  [![Downloads](https://img.shields.io/pypi/dm/saavn.py.svg?style=flat-square)](https://pypi.org/project/saavn.py/)

  [Features](#features) • [Install](#install) • [Usage](#usage) • [Contributing](#contributing) • [License](#license)
</div>

## Features

- Search and download songs, albums, playlists and artists from JioSaavn
- Interactive keyboard navigation and selection with arrow keys
- Real-time progress tracking with beautiful UI 
- High quality audio downloads (320kbps MP3)
- Support for direct JioSaavn URLs
- Configurable output directory
- Cross-platform support (Windows, macOS, Linux)

## Install

You can install Saavn.py using pip or from source:

```bash
pip install saavn.py
```

or from source:

```bash
git clone https://github.com/0xhimangshu/saavn.py
cd saavn.py
pip install -r requirements.txt
python setup.py install
```

## Usage

```bash
python -m saavn -s "https://www.jiosaavn.com/s/playlist/d106d3c2d80b4702585f0e1a41098fd4/test/PCXplErt,39xWb5,FqsjKg__" # can be a track, playlist, album or artist url 

python -m saavn -s "shape of you" -o ~/Music # searches for the track and downloads it to the specified directory
```

# Screenshots
### Main Menu
![Main Menu](./screenshots/ss-1.png)
### Searching for a track
![Search](./screenshots/ss-4.png)
### Selecting a track to download
![Download](./screenshots/ss-2.png)
### Downloading a track
![Downloading](./screenshots/ss-3.png)


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

