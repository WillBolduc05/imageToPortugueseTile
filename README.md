# imageToPencilSketch
This is a simple program to convert supplied images into portuguese-style tile murals

## Prereqs

```
pip3 install opencv-python pillow argparse
pip3 install flask
```

## Running

Parameters are `--input=<file_to_be_converted>`, `--output=<file_to_be_generated` and `--thickness=<number_1_to_5`.
Example:

```
python3 sketchConverter.py --input=sunset.jpg --output=tile.png --thickness=5
```

## Running Dockerfile
$ docker run -p 80:8000 [name of image]

## Known Issues
The coloration may look a bit off, testing is ongoing to find the optimal colors for the "bluescale" conversion

