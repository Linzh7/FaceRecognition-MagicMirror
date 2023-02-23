# FaceRecognition - Magic Mirror service

This service is aimed to recognize the person using Magic Mirror.

This module can only **run on x86**.

## Stucture of project

```
.
├── linzhutil.py - my tools collection
├── README.md - the file you are reading
├── facecompareation.py - the service
├── data - some pictures
└── requirements.txt - libraries this service need
```

## How to get started

### Requirements

Make sure that you install all libraries.

We also provide a `requirements.txt` for pip. Use the following command to install.

``pip install -r requirements.txt``

### Run service

1. Config the `SERVER_ADDRESS` and `SERVER_PORT` in `facecompareation.py`
1. If you want to use camera, modify the `TEST_PATH`
1. Run `facecompareation.py`


## Contribution

- Transport information module: [qubelka/MMM-transport](https://github.com/qubelka/MMM-transport)
- Personal agenda module: [noahwo/MMM-personal-agenda](https://github.com/noahwo/MMM-personal-agenda)
- And also the greatest contribution to this project which was from Kalle. (I copied this sentence from noahwo XD)
