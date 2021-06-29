FROM python:3.7-stretch

WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY keras_image_classification ./keras_image_classification
COPY local_binary_patterns ./local_binary_patterns
COPY detector.py .

CMD ["python3", "-u", "/app/detector.py"]

