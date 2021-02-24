# BBB Live Streaming

Streams a given BBB Meeting to an RTMP Server.

*License:*   [GNU GPL v3 or later](http://www.gnu.org/copyleft/gpl.html)

## Getting Started

### Prerequisites

All you need is Docker running on your machine and a media server to stream to.

### Configuration

You need to set some environment variables to run the container.

#### Required settings
* BBB_URL - URL to BBB including http/https e.g. https://your_BigBlueButton_server/bigbluebutton/api
* BBB_MEETING_ID - ID of the BBB Meeting (You can get the ID via an API call: https://your_bbb_server/bigbluebutton/api/getMeetings?checksum=<checksum>)
* BBB_SECRET - Secret of your BBB installation (You can get the secret with: bbb-conf --secret)
* BBB_STREAM_URL - URL of your streaming server including rtmp. Leave out to disable streaming. (e.g. rtmp://media_server_url/stream/stream_key)

#### Optional settings
* BBB_START_MEETING - start meeting
* BBB_ATTENDEE_PASSWORD - attendee password (optional - has to be set to the attendee password of moodle/greenlight or any other frontend to allow joining via their links)
* BBB_MODERATOR_PASSWORD - moderator password (optional - has to be set to the moderator password of moodle/greenlight or any other frontend to allow joining via their links)
* BBB_MEETING_TITLE - meeting title (optional - only works if the meeting is started by the liveStreaming)
* BBB_DOWNLOAD_MEETING= - download / save BigBlueButton meeting in lossless mkv format
* BBB_INTRO= - play intro file (can be a local file in videodata folder e.g. /video/intro.mp4 or a url of a mediastream e.g. https://my.intro.stream)
* BBB_BEGIN_INTRO_AT=04:40 - begin the intro at position (optional, e.g. 00:00:05)
* BBB_END_INTRO_AT= - end intro after (optional, e.g. 01:00:00 - after one hour)
* BBB_USER_NAME - the username to join the meeting. (Default: Live)
* BBB_SHOW_CHAT - shows the chat on the left side of the window (Default: false)
* BBB_RESOLUTION - the streamed/downloaded resolution (Default: 1920x1080)
* TZ - Timezone (Default: Europe/Vienna)

#### Chat settings
* BBB_ENABLE_CHAT - Enable Chat feedback channel
* BBB_REDIS_HOST - Set REDIS host (Default: redis)
* BBB_REDIS_CHANNEL - Set REDIS channel (Default: chat)
* BBB_CHAT_NAME - the username to join the meeting for chatting. (Default: Chat)
* BBB_CHAT_STREAM_URL - The URL of the stream that should be displayed in the chat (Default: rtmp:// destination)

#### Debug
* DEBUG - settings this to non-empty value will result in more verbose output

#### Advanced Usage
* FFMPEG_STREAM_THREADS - number of threads for ffmpeg during streaming (Default: 0 (auto))
* FFMPEG_STREAM_VIDEO_BITRATE - video bitrate (in k) (Default: 4000)
* FFMPEG_INPUT_THREAD_QUEUE_SIZE - `thread_queue_size` option to be passed to ffmpeg (Default: 1024)
* FFMPEG_STREAM_OPTIONS - ffmpeg options to use when streaming (bitrate/codec/...), see `stream.py` for default value
* FFMPEG_DOWNLOAD_OPTIONS - ffmpeg options to use when downloading, see `stream.py` for default value
* BROWSER_DISABLE_DEV_SHM_USAGE - whether to disable `/dev/shm` usage of the browser (default: false),
  for use cases where available /dev/shm is very limited, note that setting this to true can result in disk trashing

### Starting liveStreaming
* wget -O docker-compose.yml https://raw.github.com/aau-zid/BigBlueButton-liveStreaming/1.0.0-beta.7/examples/docker-compose.yml.example
* (change configuration)
* docker-compose up -d
* docker-compose down 

### Chat feedback
to use the user feedback via chat injection you will have to setup a website wehre the user can write comments and send them to your meeting.
In the examples folder, there are two files you can use as starting point:

* player_and_chat.php
place this in a public webpage or create a similar webform that will be send to the processing php file sendChatMessage.php

* sendChatMessage.php
this file must be reachable by the webform and has to have access to the redis database you configured in your docker-compose file.

## Known Limitations
* the streamer does not reconnect, if the connection to BigBlueButton gets lost
* when using breakoutrooms, the streamer will show the popup of the invitation and not be able to get back to the conference

## privacy policy and legal notes

Please try to follow best practices for data protection and privacy.
Take all steps to comply with privacy law principles that prohibit unlawful, opaque and limitless capture and processing of personal data. 

The GDPR (General Data Protection Regulation) provides individual rights to EU citizens in relation to personal Data.
To find out more about GDPR, please visit the [European Union’s website](https://ec.europa.eu).

The California Consumer Privacy Act (CCPA) provides certain rights to California residents in relation to their personal information. 

Similar to the GDPR and  the CCPA, other local privacy law principles  also may institute penalties for businesses that suffer data breaches due to poor security procedures.
Always be transparent and act upon privacy rights and federal law Regulations.

## License
BigBlueButton-liveStreaming is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BigBlueButton-liveStreaming is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BigBlueButton-liveStreaming.  If not, see [GNU website](https://www.gnu.org/licenses)
