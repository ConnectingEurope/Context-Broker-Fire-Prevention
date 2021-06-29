FROM python:3.7-stretch

WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY data_processor ./data_processor
COPY video_receiver.py .

CMD ["python3", "-u", "/app/video_receiver.py"]

