FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/src/app

RUN ln -s -f /bin/true /usr/bin/chfn \
    && apt-get update && apt-get install -y \
        python-is-python3 \
        python3-pip \
        python3-dev \
        xvfb \
        fluxbox \
        ffmpeg \
        dbus-x11 \
        libasound2 \
        libasound2-plugins\
        libnss-wrapper \
        alsa-utils \
        alsa-oss \
        pulseaudio \
        pulseaudio-utils \
    && mkdir /home/lithium /var/run/pulse /run/user/lithium \
    && chown -R 1001:0 /home/lithium /run/user/lithium /var/run/pulse \
    && chmod -R g=u /home/lithium /run/user/lithium /var/run/pulse

RUN  pip3 install --upgrade pip

COPY py_requirements.txt ./

RUN pip install --no-cache-dir -r py_requirements.txt



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

ENV BBB_RESOLUTION 1920x1080
ENV BBB_AS_MODERATOR false
ENV BBB_USER_NAME Live
ENV BBB_CHAT_NAME Chat
ENV BBB_SHOW_CHAT false
ENV BBB_ENABLE_CHAT false
ENV BBB_REDIS_HOST redis
ENV BBB_REDIS_CHANNEL chat
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
ENV TZ Europe/Vienna
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY stream.py ./
COPY chat.py ./
COPY startStream.sh ./
COPY docker-entrypoint.sh ./
COPY nsswrapper.sh ./

ENTRYPOINT ["sh","docker-entrypoint.sh"]

CMD ["sh","startStream.sh" ]
USER 1001
