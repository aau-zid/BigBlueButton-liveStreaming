FROM python:3

WORKDIR /usr/src/app

COPY py_requirements.txt ./

RUN pip install --no-cache-dir -r py_requirements.txt

RUN apt-get update && apt-get install -y \
        xvfb \
        ffmpeg \
        fluxbox \
        dbus-x11 \
        libasound2 \
        libasound2-plugins\
        alsa-utils \
        alsa-oss \
        pulseaudio \
        pulseaudio-utils 

RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip chromedriver* && \
    pwd && ls

ENV BBB_AS_MODERATOR false
ENV BBB_USER_NAME Live

COPY stream.py ./
COPY startStream.sh ./
COPY docker-entrypoint.sh ./

ENTRYPOINT ["sh","docker-entrypoint.sh"]

CMD ["sh","startStream.sh" ]