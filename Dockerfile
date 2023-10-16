FROM ubuntu:latest
RUN apt-get update -qy
RUN apt-get install -qy python3-pip
COPY . /app
WORKDIR /app
RUN pip install selenium==4.14.0
RUN yes | apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1
RUN yes | apt-get install -y chromium-browser
CMD ["python3","export_data_test.py"]


#error   (The process started from chrome location /root/.cache/selenium/chrome/linux64/118.0.5993.70/chrome is no longer running, so ChromeDriver is assuming that Chrome has crashed.)