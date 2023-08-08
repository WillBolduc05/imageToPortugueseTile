FROM python:3
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY sketchConverter.py .
RUN mkdir templates/
COPY templates/* templates/
RUN pip3 install opencv-python 
RUN pip3 install pillow
RUN pip3 install argparse
RUN pip3 install flask
EXPOSE 8000
CMD [ "python", "./sketchConverter.py" ]
