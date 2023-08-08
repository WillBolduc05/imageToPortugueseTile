FROM python:3
COPY Code .
RUN pip3 install opencv-python 
RUN pip3 install pillow
RUN pip3 install argparse
RUN pip3 install flask
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 8000
CMD [ "python", "./sketchConverter.py" ]
