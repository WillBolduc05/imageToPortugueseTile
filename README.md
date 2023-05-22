# imageToPencilSketch
This is a simple program to convert supplied images into blue pencil sketches on tan backgrounds. 

## Prereqs

```
pip3 install opencv-python pillow argparse
```

## Running

Parameters are `--input=<file_to_be_converted>`, `--output=<file_to_be_generated` and `--thickness=<number_1_to_5`.
Example:

```
python3 sketchConverter.py --input=sunset.jpg --output=tile.png --thickness=5
```

## Known Issues
Small details are lost very quickly, and things like clouds are not shown
The coloration may look a bit off, testing is ongoing to find the optimal colors for the "bluescale" conversion

